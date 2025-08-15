import pandas as pd
import json
from typing import List, Dict
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class KnowledgeProcessor:
    def __init__(self):
        self.raw_path = Path("../data/raw")
        self.processed_path = Path("../data/processed")
        self.processed_path.mkdir(parents=True, exist_ok=True)
    
    def process_comprehensive_food_data(self) -> pd.DataFrame:
        """Process and enhance the comprehensive food database"""
        try:
            df = pd.read_csv(self.raw_path / "comprehensive_foods.csv")
            
            # Clean and standardize
            df['food_name'] = df['food_name'].str.title()
            
            # Fill any missing values
            numeric_cols = ['calories', 'protein_g', 'carbs_g', 'fat_g', 'fiber_g', 
                          'vitamin_c_mg', 'calcium_mg', 'iron_mg']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = df[col].fillna(0)
            
            # Add nutritional density scores
            df['protein_density'] = df['protein_g'] / (df['calories'] / 100)  # g protein per 100 calories
            df['nutrient_density_score'] = (
                (df['protein_g'] / 25) +  # Based on 25g being high protein
                (df['fiber_g'] / 10) +    # Based on 10g being high fiber
                (df['vitamin_c_mg'] / 60) + # Based on 60mg being high vitamin C
                (df['calcium_mg'] / 300) +  # Based on 300mg being high calcium
                (df['iron_mg'] / 10)        # Based on 10mg being high iron
            )
            
            # Categorize foods by primary macronutrient
            conditions = [
                (df['protein_g'] >= 15) & (df['protein_g'] / df['calories'] * 4 >= 0.35),
                (df['carbs_g'] >= 15) & (df['carbs_g'] / df['calories'] * 4 >= 0.50),
                (df['fat_g'] >= 10) & (df['fat_g'] / df['calories'] * 9 >= 0.35),
            ]
            
            macro_categories = ['Protein-Rich', 'Carb-Rich', 'Fat-Rich']
            df['macro_category'] = 'Balanced'
            
            for condition, category in zip(conditions, macro_categories):
                df.loc[condition, 'macro_category'] = category
            
            # Add health benefit tags
            df['health_benefits'] = ''
            
            # High antioxidant foods
            antioxidant_foods = ['Blueberries', 'Strawberries', 'Kale', 'Spinach', 'Bell Peppers']
            df.loc[df['food_name'].str.contains('|'.join(antioxidant_foods), case=False, na=False), 
                   'health_benefits'] = df.loc[df['food_name'].str.contains('|'.join(antioxidant_foods), case=False, na=False), 
                   'health_benefits'] + 'High Antioxidants; '
            
            # Heart healthy foods
            heart_healthy = ['Salmon', 'Walnuts', 'Olive Oil', 'Avocado', 'Oats']
            df.loc[df['food_name'].str.contains('|'.join(heart_healthy), case=False, na=False), 
                   'health_benefits'] = df.loc[df['food_name'].str.contains('|'.join(heart_healthy), case=False, na=False), 
                   'health_benefits'] + 'Heart Healthy; '
            
            # Bone health foods
            bone_health = ['Kale', 'Broccoli', 'Almonds', 'Chia Seeds', 'Greek Yogurt']
            df.loc[df['food_name'].str.contains('|'.join(bone_health), case=False, na=False), 
                   'health_benefits'] = df.loc[df['food_name'].str.contains('|'.join(bone_health), case=False, na=False), 
                   'health_benefits'] + 'Bone Health; '
            
            df['health_benefits'] = df['health_benefits'].str.rstrip('; ')
            
            # Save processed data
            df.to_csv(self.processed_path / "comprehensive_foods_processed.csv", index=False)
            logger.info(f"Processed comprehensive food database with {len(df)} items")
            
            return df
            
        except Exception as e:
            logger.error(f"Error processing comprehensive food data: {e}")
            return pd.DataFrame()
    
    def create_enhanced_searchable_documents(self) -> List[Dict]:
        """Create comprehensive searchable documents for RAG system"""
        documents = []
        
        # Process food data
        food_df = self.process_comprehensive_food_data()
        
        for _, food in food_df.iterrows():
            # Create detailed food document
            doc = {
                "id": f"food_{food.get('food_code', len(documents))}",
                "type": "food_item",
                "content": self._create_detailed_food_description(food),
                "metadata": {
                    "food_name": food['food_name'],
                    "category": food.get('food_category', 'Unknown'),
                    "macro_category": food.get('macro_category', 'Balanced'),
                    "calories": food.get('calories', 0),
                    "protein": food.get('protein_g', 0),
                    "carbs": food.get('carbs_g', 0),
                    "fat": food.get('fat_g', 0),
                    "fiber": food.get('fiber_g', 0),
                    "vitamin_c": food.get('vitamin_c_mg', 0),
                    "calcium": food.get('calcium_mg', 0),
                    "iron": food.get('iron_mg', 0),
                    "nutrient_density": food.get('nutrient_density_score', 0),
                    "health_benefits": food.get('health_benefits', ''),
                    "nutrition_highlights": food.get('nutrition_highlights', '')
                }
            }
            documents.append(doc)
        
        # Add comprehensive nutrition knowledge
        try:
            with open(self.raw_path / "comprehensive_knowledge.json", "r") as f:
                knowledge = json.load(f)
            
            for i, item in enumerate(knowledge):
                doc = {
                    "id": f"knowledge_{i}",
                    "type": "nutrition_knowledge",
                    "content": f"{item['topic']}: {item['content']}",
                    "metadata": {
                        "topic": item['topic'],
                        "category": item['category'],
                        "tags": item['tags'],
                        "content_type": "guideline"
                    }
                }
                documents.append(doc)
        
        except Exception as e:
            logger.error(f"Error loading comprehensive knowledge base: {e}")
        
        # Add recipe components and meal combinations
        recipe_components = self._create_recipe_components(food_df)
        documents.extend(recipe_components)
        
        # Add meal planning templates
        meal_templates = self._create_meal_templates()
        documents.extend(meal_templates)
        
        # Save all documents
        with open(self.processed_path / "comprehensive_documents.json", "w") as f:
            json.dump(documents, f, indent=2)
        
        logger.info(f"Created {len(documents)} comprehensive searchable documents")
        return documents
    
    def _create_detailed_food_description(self, food: pd.Series) -> str:
        """Create detailed natural language description of food item"""
        name = food['food_name']
        category = food.get('food_category', 'food item')
        macro_cat = food.get('macro_category', 'balanced')
        calories = food.get('calories', 0)
        protein = food.get('protein_g', 0)
        carbs = food.get('carbs_g', 0)
        fat = food.get('fat_g', 0)
        fiber = food.get('fiber_g', 0)
        vitamin_c = food.get('vitamin_c_mg', 0)
        calcium = food.get('calcium_mg', 0)
        iron = food.get('iron_mg', 0)
        
        description = f"{name} is a {macro_cat.lower()} {category.lower()} that provides {calories} calories per 100g serving. "
        description += f"Macronutrient profile: {protein}g protein, {carbs}g carbohydrates, {fat}g fat. "
        
        # Add micronutrient information
        if vitamin_c > 10:
            description += f"Excellent source of vitamin C ({vitamin_c}mg). "
        if calcium > 50:
            description += f"Good source of calcium ({calcium}mg). "
        if iron > 1:
            description += f"Contains {iron}mg iron. "
        if fiber > 3:
            description += f"High in dietary fiber ({fiber}g). "
        
        # Add nutritional benefits
        if protein > 20:
            description += "Excellent for muscle building and repair. "
        elif protein > 10:
            description += "Good protein source for muscle maintenance. "
        
        if calories < 50:
            description += "Very low calorie option, great for weight management. "
        elif calories < 100:
            description += "Low calorie food, suitable for weight control. "
        elif calories > 400:
            description += "Calorie-dense food, use in moderation for weight management. "
        
        # Add specific food benefits
        health_benefits = food.get('health_benefits', '')
        if health_benefits:
            description += f"Health benefits include: {health_benefits.replace(';', ',')}. "
        
        # Add usage suggestions
        if category.lower() == 'fruits':
            description += "Perfect for snacking, smoothies, or adding natural sweetness to meals. "
        elif category.lower() == 'vegetables':
            description += "Excellent for salads, stir-fries, or as a nutritious side dish. "
        elif 'protein' in macro_cat.lower():
            description += "Ideal for post-workout meals or as a main protein source. "
        elif category.lower() == 'nuts & seeds':
            description += "Great for snacking, adding to yogurt, or incorporating into baked goods. "
        
        return description
    
    def _create_recipe_components(self, food_df: pd.DataFrame) -> List[Dict]:
        """Create documents for common recipe combinations"""
        recipe_docs = []
        
        recipes = [
            {
                "name": "High-Protein Breakfast Bowl",
                "ingredients": ["Greek Yogurt", "Blueberries", "Almonds", "Chia Seeds"],
                "description": "A protein-rich breakfast combining Greek yogurt with antioxidant berries and healthy fats from nuts and seeds. Provides sustained energy and supports muscle maintenance.",
                "category": "Breakfast Recipes",
                "nutrition_focus": "High Protein, Antioxidants"
            },
            {
                "name": "Post-Workout Recovery Smoothie",
                "ingredients": ["Banana", "Greek Yogurt", "Spinach", "Chia Seeds"],
                "description": "Optimal post-workout nutrition combining quick carbs from banana, protein from yogurt, and micronutrients from spinach. Perfect 3:1 carb to protein ratio for recovery.",
                "category": "Sports Nutrition",
                "nutrition_focus": "Recovery, Protein, Carbohydrates"
            },
            {
                "name": "Heart-Healthy Salad",
                "ingredients": ["Salmon", "Avocado", "Kale", "Walnuts", "Olive Oil"],
                "description": "A heart-healthy meal rich in omega-3 fatty acids from salmon and walnuts, monounsaturated fats from avocado and olive oil, plus antioxidants from kale.",
                "category": "Main Meals",
                "nutrition_focus": "Heart Health, Omega-3, Antioxidants"
            }
        ]
        
        for i, recipe in enumerate(recipes):
            doc = {
                "id": f"recipe_{i}",
                "type": "recipe_combination",
                "content": f"{recipe['name']}: {recipe['description']} Main ingredients: {', '.join(recipe['ingredients'])}.",
                "metadata": {
                    "recipe_name": recipe['name'],
                    "ingredients": recipe['ingredients'],
                    "category": recipe['category'],
                    "nutrition_focus": recipe['nutrition_focus'],
                    "content_type": "recipe"
                }
            }
            recipe_docs.append(doc)
        
        return recipe_docs
    
    def _create_meal_templates(self) -> List[Dict]:
        """Create meal planning template documents"""
        templates = [
            {
                "name": "Weight Loss Meal Template",
                "content": "For sustainable weight loss, create meals with lean protein (25-30% calories), non-starchy vegetables (unlimited), moderate complex carbs (25-30% calories), and healthy fats (20-25% calories). Examples: Grilled chicken with roasted vegetables and quinoa, or salmon salad with avocado.",
                "category": "Meal Planning",
                "tags": ["weight loss", "meal planning", "macronutrients"]
            },
            {
                "name": "Muscle Building Meal Template", 
                "content": "For muscle gain, ensure adequate protein (1.6-2.2g/kg body weight), sufficient carbohydrates for energy (45-55% calories), and healthy fats (20-30% calories). Include protein at every meal and snack. Examples: Oatmeal with protein powder and berries, or lean beef with sweet potato.",
                "category": "Meal Planning",
                "tags": ["muscle building", "protein", "meal planning"]
            },
            {
                "name": "Anti-Inflammatory Meal Template",
                "content": "Focus on colorful vegetables, fatty fish, nuts, seeds, and olive oil while limiting processed foods and added sugars. Examples: Turmeric-spiced salmon with roasted rainbow vegetables, or a spinach salad with walnuts and berries.",
                "category": "Meal Planning", 
                "tags": ["anti-inflammatory", "omega-3", "antioxidants"]
            }
        ]
        
        template_docs = []
        for i, template in enumerate(templates):
            doc = {
                "id": f"template_{i}",
                "type": "meal_template",
                "content": f"{template['name']}: {template['content']}",
                "metadata": {
                    "template_name": template['name'],
                    "category": template['category'],
                    "tags": template['tags'],
                    "content_type": "template"
                }
            }
            template_docs.append(doc)
        
        return template_docs

if __name__ == "__main__":
    processor = KnowledgeProcessor()
    documents = processor.create_enhanced_searchable_documents()
    print(f"✅ Enhanced knowledge processing complete!")
    print(f"📄 Total documents created: {len(documents)}")
    
    # Print summary
    doc_types = {}
    for doc in documents:
        doc_type = doc['type']
        doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
    
    print(f"📊 Document breakdown:")
    for doc_type, count in doc_types.items():
        print(f"   {doc_type}: {count}")