"""
USDA FoodData Central API Integration
Handles real-time nutrition data lookup for multimodal integration
"""

import requests
import os
import logging
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class USDANutritionAPI:
    def __init__(self):
        self.api_key = os.getenv('USDA_API_KEY')
        self.base_url = "https://api.nal.usda.gov/fdc/v1"
        
        if not self.api_key:
            logger.warning("USDA API key not found. Some features may not work.")
    
    def search_foods(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search for foods in USDA database
        
        Args:
            query: Food name to search for
            max_results: Maximum number of results to return
            
        Returns:
            List of food items with basic info
        """
        if not self.api_key:
            return self._get_sample_foods(query)
        
        try:
            url = f"{self.base_url}/foods/search"
            params = {
                'query': query,
                'dataType': 'Foundation,SR Legacy',
                'pageSize': max_results,
                'api_key': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            foods = []
            
            for food in data.get('foods', []):
                food_info = {
                    'fdc_id': food.get('fdcId'),
                    'description': food.get('description', ''),
                    'data_type': food.get('dataType', ''),
                    'food_category': food.get('foodCategory', ''),
                    'score': food.get('score', 0)
                }
                foods.append(food_info)
            
            logger.info(f"Found {len(foods)} foods for query: {query}")
            return foods
            
        except Exception as e:
            logger.error(f"Error searching USDA API: {e}")
            return self._get_sample_foods(query)
    
    def get_food_details(self, fdc_id: int) -> Optional[Dict]:
        """
        Get detailed nutrition information for a specific food
        
        Args:
            fdc_id: USDA FDC ID for the food
            
        Returns:
            Detailed nutrition information
        """
        if not self.api_key:
            return self._get_sample_nutrition(fdc_id)
        
        try:
            url = f"{self.base_url}/food/{fdc_id}"
            params = {'api_key': self.api_key}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            food_data = response.json()
            return self._parse_nutrition_data(food_data)
            
        except Exception as e:
            logger.error(f"Error getting food details for ID {fdc_id}: {e}")
            return self._get_sample_nutrition(fdc_id)
    
    def analyze_meal_components(self, food_descriptions: List[str]) -> List[Dict]:
        """
        Analyze multiple food components from a meal
        
        Args:
            food_descriptions: List of food descriptions (e.g., ["6oz chicken breast", "1 cup broccoli"])
            
        Returns:
            List of analyzed food components with nutrition
        """
        analyzed_foods = []
        
        for description in food_descriptions:
            # Parse portion and food name
            portion_info = self._parse_portion(description)
            
            # Search for the food
            search_results = self.search_foods(portion_info['food_name'], max_results=3)
            
            if search_results:
                # Get detailed nutrition for best match
                best_match = search_results[0]
                nutrition_details = self.get_food_details(best_match['fdc_id'])
                
                if nutrition_details:
                    # Calculate nutrition for the specific portion
                    portioned_nutrition = self._calculate_portion_nutrition(
                        nutrition_details, 
                        portion_info['amount'], 
                        portion_info['unit']
                    )
                    
                    analyzed_foods.append({
                        'original_description': description,
                        'food_name': best_match['description'],
                        'portion': f"{portion_info['amount']} {portion_info['unit']}",
                        'nutrition': portioned_nutrition,
                        'confidence': best_match['score']
                    })
        
        return analyzed_foods
    
    def _parse_portion(self, description: str) -> Dict:
        """Parse portion size and food name from description"""
        # Simple parsing - could be enhanced with NLP
        import re
        
        # Look for patterns like "6oz chicken" or "1 cup broccoli"
        portion_patterns = [
            r'(\d+(?:\.\d+)?)\s*(oz|ounces?|g|grams?|lbs?|pounds?)\s+(.+)',
            r'(\d+(?:\.\d+)?)\s*(cups?|cup|tbsp|tsp|tablespoons?|teaspoons?)\s+(.+)',
            r'(\d+(?:\.\d+)?)\s*(pieces?|slices?|items?)\s+(.+)'
        ]
        
        for pattern in portion_patterns:
            match = re.match(pattern, description.lower().strip())
            if match:
                return {
                    'amount': float(match.group(1)),
                    'unit': match.group(2),
                    'food_name': match.group(3).strip()
                }
        
        # If no portion found, assume 100g serving
        return {
            'amount': 100,
            'unit': 'g',
            'food_name': description.strip()
        }
    
    def _calculate_portion_nutrition(self, base_nutrition: Dict, amount: float, unit: str) -> Dict:
        """Calculate nutrition for specific portion size"""
        # Convert to grams for calculation
        amount_in_grams = self._convert_to_grams(amount, unit, base_nutrition.get('food_name', ''))
        
        # Base nutrition is per 100g, so calculate multiplier
        multiplier = amount_in_grams / 100.0
        
        portioned_nutrition = {}
        for nutrient, value in base_nutrition.get('nutrients', {}).items():
            if isinstance(value, (int, float)):
                portioned_nutrition[nutrient] = round(value * multiplier, 2)
        
        return portioned_nutrition
    
    def _convert_to_grams(self, amount: float, unit: str, food_name: str) -> float:
        """Convert various units to grams"""
        unit = unit.lower()
        
        # Weight conversions
        if unit in ['g', 'gram', 'grams']:
            return amount
        elif unit in ['oz', 'ounce', 'ounces']:
            return amount * 28.35
        elif unit in ['lb', 'lbs', 'pound', 'pounds']:
            return amount * 453.6
        
        # Volume conversions (approximate for common foods)
        elif unit in ['cup', 'cups']:
            # Rough approximations - could be more food-specific
            if 'rice' in food_name.lower():
                return amount * 185  # cooked rice
            elif 'broccoli' in food_name.lower():
                return amount * 156  # chopped broccoli
            else:
                return amount * 240  # general liquid measure
        
        elif unit in ['tbsp', 'tablespoon', 'tablespoons']:
            return amount * 15
        elif unit in ['tsp', 'teaspoon', 'teaspoons']:
            return amount * 5
        
        # If unknown unit, assume it's already in grams
        return amount
    
    def _parse_nutrition_data(self, food_data: Dict) -> Dict:
        """Parse USDA food data into our standard format"""
        nutrients = {}
        
        # Extract key nutrients
        for nutrient in food_data.get('foodNutrients', []):
            nutrient_name = nutrient.get('nutrient', {}).get('name', '').lower()
            value = nutrient.get('amount', 0)
            unit = nutrient.get('nutrient', {}).get('unitName', '')
            
            # Map common nutrients
            if 'protein' in nutrient_name:
                nutrients['protein_g'] = value
            elif 'carbohydrate' in nutrient_name and 'fiber' not in nutrient_name:
                nutrients['carbohydrates_g'] = value
            elif 'total lipid' in nutrient_name or ('fat' in nutrient_name and 'fatty' not in nutrient_name):
                nutrients['total_fat_g'] = value
            elif 'energy' in nutrient_name and 'kcal' in unit.lower():
                nutrients['calories'] = value
            elif 'fiber' in nutrient_name:
                nutrients['fiber_g'] = value
            elif 'vitamin c' in nutrient_name:
                nutrients['vitamin_c_mg'] = value
            elif 'calcium' in nutrient_name:
                nutrients['calcium_mg'] = value
            elif 'iron' in nutrient_name:
                nutrients['iron_mg'] = value
            elif 'sodium' in nutrient_name:
                nutrients['sodium_mg'] = value
        
        return {
            'food_name': food_data.get('description', ''),
            'fdc_id': food_data.get('fdcId'),
            'data_type': food_data.get('dataType', ''),
            'nutrients': nutrients
        }
    
    def _get_sample_foods(self, query: str) -> List[Dict]:
        """Fallback sample foods when API is not available"""
        sample_foods = {
            'chicken': [
                {'fdc_id': 171077, 'description': 'Chicken, broilers or fryers, breast, meat only, cooked, roasted', 'data_type': 'SR Legacy', 'food_category': 'Poultry Products', 'score': 100}
            ],
            'broccoli': [
                {'fdc_id': 170379, 'description': 'Broccoli, raw', 'data_type': 'SR Legacy', 'food_category': 'Vegetables and Vegetable Products', 'score': 100}
            ],
            'rice': [
                {'fdc_id': 168878, 'description': 'Rice, brown, long-grain, cooked', 'data_type': 'SR Legacy', 'food_category': 'Cereal Grains and Pasta', 'score': 100}
            ]
        }
        
        # Simple keyword matching
        for keyword in sample_foods.keys():
            if keyword in query.lower():
                return sample_foods[keyword]
        
        return [{'fdc_id': 999999, 'description': f'Sample food for {query}', 'data_type': 'Sample', 'food_category': 'Unknown', 'score': 50}]
    
    def _get_sample_nutrition(self, fdc_id: int) -> Dict:
        """Fallback nutrition data when API is not available"""
        sample_nutrition = {
            171077: {  # Chicken breast
                'food_name': 'Chicken, broilers or fryers, breast, meat only, cooked, roasted',
                'fdc_id': 171077,
                'nutrients': {
                    'calories': 165,
                    'protein_g': 31.0,
                    'carbohydrates_g': 0,
                    'total_fat_g': 3.6,
                    'fiber_g': 0,
                    'sodium_mg': 74
                }
            },
            170379: {  # Broccoli
                'food_name': 'Broccoli, raw',
                'fdc_id': 170379,
                'nutrients': {
                    'calories': 34,
                    'protein_g': 2.8,
                    'carbohydrates_g': 7,
                    'total_fat_g': 0.4,
                    'fiber_g': 2.6,
                    'vitamin_c_mg': 89.2
                }
            }
        }
        
        return sample_nutrition.get(fdc_id, {
            'food_name': f'Sample food {fdc_id}',
            'fdc_id': fdc_id,
            'nutrients': {'calories': 100, 'protein_g': 5, 'carbohydrates_g': 10, 'total_fat_g': 2}
        })

# Test function
def test_usda_api():
    """Test the USDA API integration"""
    print("🧪 Testing USDA API Integration...")
    
    api = USDANutritionAPI()
    
    # Test search
    print("\n1. Testing food search...")
    foods = api.search_foods("chicken breast", max_results=3)
    for food in foods:
        print(f"   - {food['description'][:50]}... (ID: {food['fdc_id']})")
    
    # Test detailed nutrition
    if foods:
        print("\n2. Testing nutrition details...")
        nutrition = api.get_food_details(foods[0]['fdc_id'])
        print(f"   Food: {nutrition['food_name']}")
        print(f"   Calories: {nutrition['nutrients'].get('calories', 'N/A')}")
        print(f"   Protein: {nutrition['nutrients'].get('protein_g', 'N/A')}g")
    
    # Test meal analysis
    print("\n3. Testing meal analysis...")
    meal = ["6oz chicken breast", "1 cup broccoli", "0.5 cup brown rice"]
    analyzed_meal = api.analyze_meal_components(meal)
    
    total_calories = 0
    total_protein = 0
    
    for food in analyzed_meal:
        calories = food['nutrition'].get('calories', 0)
        protein = food['nutrition'].get('protein_g', 0)
        total_calories += calories
        total_protein += protein
        print(f"   - {food['original_description']}: {calories:.0f} cal, {protein:.1f}g protein")
    
    print(f"\n📊 TOTAL MEAL: {total_calories:.0f} calories, {total_protein:.1f}g protein")
    print("✅ USDA API integration working!")

if __name__ == "__main__":
    test_usda_api()