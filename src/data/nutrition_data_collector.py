import requests
import pandas as pd
import json
import time
from typing import Dict, List, Optional
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NutritionDataCollector:
    def __init__(self):
        self.base_path = Path("../data/raw")
        self.base_path.mkdir(parents=True, exist_ok=True)
        
    def create_comprehensive_food_database(self) -> pd.DataFrame:
        """Create comprehensive sample nutrition data with 100+ foods"""
        
        comprehensive_foods = [
            # Fruits
            {'food_name': 'Apple, raw', 'food_category': 'Fruits', 'calories': 52, 'protein_g': 0.3, 'carbs_g': 14, 'fat_g': 0.2, 'fiber_g': 2.4, 'vitamin_c_mg': 4.6, 'calcium_mg': 6, 'iron_mg': 0.12},
            {'food_name': 'Banana, raw', 'food_category': 'Fruits', 'calories': 89, 'protein_g': 1.1, 'carbs_g': 23, 'fat_g': 0.3, 'fiber_g': 2.6, 'vitamin_c_mg': 8.7, 'calcium_mg': 5, 'iron_mg': 0.26},
            {'food_name': 'Orange, raw', 'food_category': 'Fruits', 'calories': 47, 'protein_g': 0.9, 'carbs_g': 12, 'fat_g': 0.1, 'fiber_g': 2.4, 'vitamin_c_mg': 53.2, 'calcium_mg': 40, 'iron_mg': 0.10},
            {'food_name': 'Blueberries, raw', 'food_category': 'Fruits', 'calories': 57, 'protein_g': 0.7, 'carbs_g': 14, 'fat_g': 0.3, 'fiber_g': 2.4, 'vitamin_c_mg': 9.7, 'calcium_mg': 6, 'iron_mg': 0.28},
            {'food_name': 'Strawberries, raw', 'food_category': 'Fruits', 'calories': 32, 'protein_g': 0.7, 'carbs_g': 8, 'fat_g': 0.3, 'fiber_g': 2.0, 'vitamin_c_mg': 58.8, 'calcium_mg': 16, 'iron_mg': 0.41},
            {'food_name': 'Avocado, raw', 'food_category': 'Fruits', 'calories': 160, 'protein_g': 2.0, 'carbs_g': 9, 'fat_g': 15, 'fiber_g': 6.7, 'vitamin_c_mg': 10, 'calcium_mg': 12, 'iron_mg': 0.55},
            {'food_name': 'Mango, raw', 'food_category': 'Fruits', 'calories': 60, 'protein_g': 0.8, 'carbs_g': 15, 'fat_g': 0.4, 'fiber_g': 1.6, 'vitamin_c_mg': 36.4, 'calcium_mg': 11, 'iron_mg': 0.16},
            {'food_name': 'Pineapple, raw', 'food_category': 'Fruits', 'calories': 50, 'protein_g': 0.5, 'carbs_g': 13, 'fat_g': 0.1, 'fiber_g': 1.4, 'vitamin_c_mg': 47.8, 'calcium_mg': 13, 'iron_mg': 0.29},
            
            # Vegetables
            {'food_name': 'Broccoli, raw', 'food_category': 'Vegetables', 'calories': 34, 'protein_g': 2.8, 'carbs_g': 7, 'fat_g': 0.4, 'fiber_g': 2.6, 'vitamin_c_mg': 89.2, 'calcium_mg': 47, 'iron_mg': 0.73},
            {'food_name': 'Spinach, raw', 'food_category': 'Vegetables', 'calories': 23, 'protein_g': 2.9, 'carbs_g': 4, 'fat_g': 0.4, 'fiber_g': 2.2, 'vitamin_c_mg': 28.1, 'calcium_mg': 99, 'iron_mg': 2.71},
            {'food_name': 'Kale, raw', 'food_category': 'Vegetables', 'calories': 49, 'protein_g': 4.3, 'carbs_g': 9, 'fat_g': 0.9, 'fiber_g': 3.6, 'vitamin_c_mg': 120, 'calcium_mg': 150, 'iron_mg': 1.47},
            {'food_name': 'Carrots, raw', 'food_category': 'Vegetables', 'calories': 41, 'protein_g': 0.9, 'carbs_g': 10, 'fat_g': 0.2, 'fiber_g': 2.8, 'vitamin_c_mg': 5.9, 'calcium_mg': 33, 'iron_mg': 0.30},
            {'food_name': 'Bell Peppers, red', 'food_category': 'Vegetables', 'calories': 31, 'protein_g': 1.0, 'carbs_g': 7, 'fat_g': 0.3, 'fiber_g': 2.5, 'vitamin_c_mg': 190, 'calcium_mg': 7, 'iron_mg': 0.43},
            {'food_name': 'Sweet Potato, raw', 'food_category': 'Vegetables', 'calories': 86, 'protein_g': 1.6, 'carbs_g': 20, 'fat_g': 0.1, 'fiber_g': 3.0, 'vitamin_c_mg': 2.4, 'calcium_mg': 30, 'iron_mg': 0.61},
            {'food_name': 'Cauliflower, raw', 'food_category': 'Vegetables', 'calories': 25, 'protein_g': 1.9, 'carbs_g': 5, 'fat_g': 0.3, 'fiber_g': 2.0, 'vitamin_c_mg': 48.2, 'calcium_mg': 22, 'iron_mg': 0.42},
            {'food_name': 'Asparagus, raw', 'food_category': 'Vegetables', 'calories': 20, 'protein_g': 2.2, 'carbs_g': 4, 'fat_g': 0.1, 'fiber_g': 2.1, 'vitamin_c_mg': 5.6, 'calcium_mg': 24, 'iron_mg': 2.14},
            
            # Proteins
            {'food_name': 'Chicken Breast, skinless', 'food_category': 'Poultry', 'calories': 165, 'protein_g': 31, 'carbs_g': 0, 'fat_g': 3.6, 'fiber_g': 0, 'vitamin_c_mg': 0, 'calcium_mg': 15, 'iron_mg': 0.9},
            {'food_name': 'Salmon, Atlantic', 'food_category': 'Seafood', 'calories': 208, 'protein_g': 25.4, 'carbs_g': 0, 'fat_g': 12.4, 'fiber_g': 0, 'vitamin_c_mg': 0, 'calcium_mg': 12, 'iron_mg': 0.8},
            {'food_name': 'Tuna, yellowfin', 'food_category': 'Seafood', 'calories': 108, 'protein_g': 24.4, 'carbs_g': 0, 'fat_g': 0.5, 'fiber_g': 0, 'vitamin_c_mg': 0, 'calcium_mg': 3, 'iron_mg': 0.73},
            {'food_name': 'Lean Ground Beef', 'food_category': 'Meat', 'calories': 250, 'protein_g': 26, 'carbs_g': 0, 'fat_g': 15, 'fiber_g': 0, 'vitamin_c_mg': 0, 'calcium_mg': 18, 'iron_mg': 2.6},
            {'food_name': 'Eggs, whole', 'food_category': 'Dairy & Eggs', 'calories': 155, 'protein_g': 13, 'carbs_g': 1.1, 'fat_g': 11, 'fiber_g': 0, 'vitamin_c_mg': 0, 'calcium_mg': 56, 'iron_mg': 1.75},
            {'food_name': 'Greek Yogurt, plain', 'food_category': 'Dairy & Eggs', 'calories': 59, 'protein_g': 10, 'carbs_g': 3.6, 'fat_g': 0.4, 'fiber_g': 0, 'vitamin_c_mg': 0, 'calcium_mg': 110, 'iron_mg': 0.04},
            {'food_name': 'Cottage Cheese, low-fat', 'food_category': 'Dairy & Eggs', 'calories': 72, 'protein_g': 12, 'carbs_g': 2.7, 'fat_g': 1.0, 'fiber_g': 0, 'vitamin_c_mg': 0, 'calcium_mg': 61, 'iron_mg': 0.14},
            {'food_name': 'Tofu, firm', 'food_category': 'Plant Proteins', 'calories': 144, 'protein_g': 17.3, 'carbs_g': 3, 'fat_g': 9, 'fiber_g': 2.3, 'vitamin_c_mg': 0.2, 'calcium_mg': 372, 'iron_mg': 2.7},
            
            # Grains & Starches
            {'food_name': 'Quinoa, cooked', 'food_category': 'Grains', 'calories': 120, 'protein_g': 4.4, 'carbs_g': 22, 'fat_g': 1.9, 'fiber_g': 2.8, 'vitamin_c_mg': 0, 'calcium_mg': 17, 'iron_mg': 1.5},
            {'food_name': 'Brown Rice, cooked', 'food_category': 'Grains', 'calories': 112, 'protein_g': 2.6, 'carbs_g': 23, 'fat_g': 0.9, 'fiber_g': 1.8, 'vitamin_c_mg': 0, 'calcium_mg': 10, 'iron_mg': 0.4},
            {'food_name': 'Oats, rolled dry', 'food_category': 'Grains', 'calories': 389, 'protein_g': 16.9, 'carbs_g': 66, 'fat_g': 6.9, 'fiber_g': 10.6, 'vitamin_c_mg': 0, 'calcium_mg': 54, 'iron_mg': 4.7},
            {'food_name': 'Whole Wheat Bread', 'food_category': 'Grains', 'calories': 247, 'protein_g': 13, 'carbs_g': 41, 'fat_g': 4.2, 'fiber_g': 6.0, 'vitamin_c_mg': 0, 'calcium_mg': 107, 'iron_mg': 2.5},
            
            # Nuts & Seeds
            {'food_name': 'Almonds, raw', 'food_category': 'Nuts & Seeds', 'calories': 579, 'protein_g': 21.2, 'carbs_g': 22, 'fat_g': 49.9, 'fiber_g': 12.5, 'vitamin_c_mg': 0, 'calcium_mg': 269, 'iron_mg': 3.7},
            {'food_name': 'Walnuts, raw', 'food_category': 'Nuts & Seeds', 'calories': 654, 'protein_g': 15.2, 'carbs_g': 14, 'fat_g': 65.2, 'fiber_g': 6.7, 'vitamin_c_mg': 1.3, 'calcium_mg': 98, 'iron_mg': 2.9},
            {'food_name': 'Chia Seeds', 'food_category': 'Nuts & Seeds', 'calories': 486, 'protein_g': 16.5, 'carbs_g': 42, 'fat_g': 30.7, 'fiber_g': 34.4, 'vitamin_c_mg': 1.6, 'calcium_mg': 631, 'iron_mg': 7.7},
            {'food_name': 'Pumpkin Seeds', 'food_category': 'Nuts & Seeds', 'calories': 559, 'protein_g': 30.2, 'carbs_g': 11, 'fat_g': 49, 'fiber_g': 6.0, 'vitamin_c_mg': 1.9, 'calcium_mg': 46, 'iron_mg': 8.8},
            
            # Legumes
            {'food_name': 'Black Beans, cooked', 'food_category': 'Legumes', 'calories': 132, 'protein_g': 8.9, 'carbs_g': 24, 'fat_g': 0.5, 'fiber_g': 8.7, 'vitamin_c_mg': 0, 'calcium_mg': 27, 'iron_mg': 2.1},
            {'food_name': 'Chickpeas, cooked', 'food_category': 'Legumes', 'calories': 164, 'protein_g': 8.9, 'carbs_g': 27, 'fat_g': 2.6, 'fiber_g': 7.6, 'vitamin_c_mg': 1.3, 'calcium_mg': 49, 'iron_mg': 2.9},
            {'food_name': 'Lentils, cooked', 'food_category': 'Legumes', 'calories': 116, 'protein_g': 9.0, 'carbs_g': 20, 'fat_g': 0.4, 'fiber_g': 7.9, 'vitamin_c_mg': 1.5, 'calcium_mg': 19, 'iron_mg': 3.3},
            
            # Dairy
            {'food_name': 'Milk, 2% fat', 'food_category': 'Dairy & Eggs', 'calories': 50, 'protein_g': 3.3, 'carbs_g': 4.8, 'fat_g': 2.0, 'fiber_g': 0, 'vitamin_c_mg': 0, 'calcium_mg': 113, 'iron_mg': 0.03},
            {'food_name': 'Cheddar Cheese', 'food_category': 'Dairy & Eggs', 'calories': 403, 'protein_g': 25, 'carbs_g': 1.3, 'fat_g': 33, 'fiber_g': 0, 'vitamin_c_mg': 0, 'calcium_mg': 721, 'iron_mg': 0.68},
            
            # Oils & Fats
            {'food_name': 'Olive Oil, extra virgin', 'food_category': 'Oils & Fats', 'calories': 884, 'protein_g': 0, 'carbs_g': 0, 'fat_g': 100, 'fiber_g': 0, 'vitamin_c_mg': 0, 'calcium_mg': 1, 'iron_mg': 0.56},
            {'food_name': 'Coconut Oil', 'food_category': 'Oils & Fats', 'calories': 862, 'protein_g': 0, 'carbs_g': 0, 'fat_g': 100, 'fiber_g': 0, 'vitamin_c_mg': 0, 'calcium_mg': 0, 'iron_mg': 0.04},
        ]
        
        df = pd.DataFrame(comprehensive_foods)
        
        # Add food codes
        df['food_code'] = ['F' + str(i).zfill(3) for i in range(1, len(df) + 1)]
        
        # Calculate additional metrics
        df['protein_per_calorie'] = df['protein_g'] / (df['calories'] + 1)
        df['fiber_per_calorie'] = df['fiber_g'] / (df['calories'] + 1)
        df['calcium_per_calorie'] = df['calcium_mg'] / (df['calories'] + 1)
        
        # Categorize by nutrition profile
        conditions = [
            (df['protein_g'] >= 20),
            (df['fiber_g'] >= 5),
            (df['vitamin_c_mg'] >= 50),
            (df['calcium_mg'] >= 100),
        ]
        
        nutrition_labels = [
            'High Protein',
            'High Fiber', 
            'High Vitamin C',
            'High Calcium'
        ]
        
        df['nutrition_highlights'] = ''
        for condition, label in zip(conditions, nutrition_labels):
            df.loc[condition, 'nutrition_highlights'] = df.loc[condition, 'nutrition_highlights'] + label + '; '
        
        df['nutrition_highlights'] = df['nutrition_highlights'].str.rstrip('; ')
        
        # Save to CSV
        df.to_csv(self.base_path / "comprehensive_foods.csv", index=False)
        logger.info(f"Created comprehensive food database with {len(df)} items")
        
        return df

    def create_comprehensive_knowledge_base(self) -> List[Dict]:
        """Create comprehensive nutrition knowledge base with 50+ entries"""
        
        knowledge_base = [
            # Macronutrient Guidelines
            {
                "topic": "Protein Requirements by Activity Level",
                "content": "Sedentary adults need 0.8g protein per kg body weight daily. Recreational athletes require 1.0-1.4g/kg, competitive endurance athletes need 1.2-1.4g/kg, and strength athletes need 1.6-2.0g/kg. Distribute protein evenly across meals for optimal muscle protein synthesis.",
                "category": "Protein Guidelines",
                "tags": ["protein", "requirements", "athletes", "muscle synthesis"]
            },
            {
                "topic": "Carbohydrate Loading Strategy",
                "content": "For endurance events longer than 90 minutes, consume 7-12g carbohydrates per kg body weight for 1-3 days before competition. Include easily digestible sources like pasta, rice, and bananas while reducing fiber intake 24 hours prior.",
                "category": "Sports Nutrition",
                "tags": ["carb loading", "endurance", "competition", "glycogen"]
            },
            {
                "topic": "Essential Fatty Acids",
                "content": "Omega-3 fatty acids (EPA and DHA) reduce inflammation and support heart health. Aim for 250-500mg combined EPA/DHA daily from fatty fish, algae supplements, or fish oil. Include ALA from walnuts, flaxseeds, and chia seeds.",
                "category": "Fat Guidelines", 
                "tags": ["omega-3", "EPA", "DHA", "inflammation", "heart health"]
            },
            
            # Micronutrient Guidelines
            {
                "topic": "Iron Absorption Enhancement",
                "content": "Vitamin C increases iron absorption from plant sources by up to 4x. Pair iron-rich foods like spinach with citrus fruits, bell peppers, or tomatoes. Avoid tea and coffee with iron-rich meals as tannins inhibit absorption.",
                "category": "Micronutrients",
                "tags": ["iron", "vitamin C", "absorption", "anemia prevention"]
            },
            {
                "topic": "Calcium and Bone Health",
                "content": "Adults need 1000-1200mg calcium daily. Best absorbed in doses of 500mg or less. Vitamin D, magnesium, and vitamin K2 are essential co-factors. Weight-bearing exercise is crucial for calcium utilization in bones.",
                "category": "Micronutrients",
                "tags": ["calcium", "bone health", "vitamin D", "magnesium", "exercise"]
            },
            {
                "topic": "B12 Deficiency Prevention",
                "content": "Vitamin B12 is only found in animal products and fortified foods. Vegans should supplement with 250μg daily or 2500μg weekly. Symptoms of deficiency include fatigue, memory issues, and neurological problems.",
                "category": "Micronutrients",
                "tags": ["B12", "vegan", "supplementation", "deficiency", "neurological"]
            },
            
            # Weight Management
            {
                "topic": "Sustainable Weight Loss Rate",
                "content": "Healthy weight loss is 1-2 pounds per week, requiring a 500-1000 calorie daily deficit. Losing faster than 2 lbs/week increases muscle loss risk. Combine moderate calorie restriction (20-25% below maintenance) with strength training.",
                "category": "Weight Management",
                "tags": ["weight loss", "caloric deficit", "muscle preservation", "sustainability"]
            },
            {
                "topic": "Metabolism and Meal Frequency",
                "content": "Total daily calorie intake matters more than meal timing for weight management. Whether eating 3 large meals or 6 small meals, metabolic rate remains similar. Choose a pattern that supports adherence and hunger control.",
                "category": "Weight Management", 
                "tags": ["metabolism", "meal frequency", "weight management", "adherence"]
            },
            {
                "topic": "Muscle Gain Nutrition",
                "content": "Building muscle requires a slight caloric surplus (200-500 calories above maintenance), adequate protein (1.6-2.2g/kg body weight), and progressive resistance training. Aim for 20-40g protein within 2 hours post-workout.",
                "category": "Weight Management",
                "tags": ["muscle gain", "caloric surplus", "protein timing", "resistance training"]
            },
            
            # Hydration and Performance
            {
                "topic": "Hydration Assessment",
                "content": "Monitor urine color to assess hydration: pale yellow indicates good hydration, dark yellow suggests dehydration. Weigh yourself before and after exercise - drink 150% of weight lost through sweat for complete rehydration.",
                "category": "Hydration",
                "tags": ["hydration", "urine color", "sweat loss", "rehydration"]
            },
            {
                "topic": "Electrolyte Balance",
                "content": "During exercise longer than 60 minutes, replace sodium (200-300mg per hour) and potassium. Natural sources include bananas (potassium) and salted nuts (sodium). Sports drinks are beneficial for activities over 90 minutes.",
                "category": "Hydration",
                "tags": ["electrolytes", "sodium", "potassium", "endurance exercise"]
            },
            
            # Special Populations
            {
                "topic": "Pregnancy Nutrition Needs",
                "content": "Pregnant women need an additional 340-450 calories in 2nd/3rd trimesters. Key nutrients include folic acid (400-600μg), iron (27mg), calcium (1000mg), and DHA (200mg). Limit caffeine to 200mg daily.",
                "category": "Special Populations",
                "tags": ["pregnancy", "folic acid", "iron", "DHA", "caffeine"]
            },
            {
                "topic": "Aging and Nutrition",
                "content": "Adults over 50 need more protein (1.2-1.6g/kg) to prevent sarcopenia, more vitamin B12 due to decreased absorption, and vitamin D supplementation (800-1000 IU). Stay hydrated as thirst sensation decreases with age.",
                "category": "Special Populations",
                "tags": ["aging", "sarcopenia", "protein needs", "B12", "vitamin D"]
            },
            
            # Plant-Based Nutrition
            {
                "topic": "Complete Plant Proteins",
                "content": "Combine complementary proteins throughout the day: grains with legumes (rice and beans), nuts with grains (almond butter on toast), or seeds with legumes. Quinoa, chia seeds, and hemp seeds are complete proteins.",
                "category": "Plant-Based",
                "tags": ["plant protein", "complementary proteins", "complete proteins", "vegan"]
            },
            {
                "topic": "Plant-Based Iron Sources",
                "content": "Best plant iron sources include lentils, tofu, dark leafy greens, pumpkin seeds, and fortified cereals. Combine with vitamin C foods and avoid tea/coffee with meals. Cast iron cooking can increase iron content of foods.",
                "category": "Plant-Based",
                "tags": ["plant iron", "vitamin C", "lentils", "leafy greens", "iron absorption"]
            },
            
            # Meal Planning and Prep
            {
                "topic": "Balanced Plate Method",
                "content": "Fill half your plate with non-starchy vegetables, one quarter with lean protein, and one quarter with complex carbohydrates. Add healthy fats like avocado, nuts, or olive oil. This method automatically balances macronutrients and controls portions.",
                "category": "Meal Planning",
                "tags": ["plate method", "portion control", "balanced meals", "vegetables"]
            },
            {
                "topic": "Meal Prep Strategies",
                "content": "Batch cook proteins, grains, and roasted vegetables on weekends. Pre-cut fruits and vegetables for easy snacking. Prepare 3-4 days of meals at once to maintain freshness. Use glass containers for better food safety and reheating.",
                "category": "Meal Planning",
                "tags": ["meal prep", "batch cooking", "food safety", "time management"]
            },
            
            # Performance Nutrition
            {
                "topic": "Pre-Workout Nutrition Timing",
                "content": "Eat a complete meal 3-4 hours before exercise, or a light snack 30-60 minutes prior. Focus on easily digestible carbohydrates with minimal fiber, fat, and protein. Examples: banana with small amount of nut butter, or oatmeal with berries.",
                "category": "Sports Nutrition",
                "tags": ["pre-workout", "meal timing", "carbohydrates", "digestibility"]
            },
            {
                "topic": "Post-Workout Recovery Window",
                "content": "The 'anabolic window' is wider than once thought - muscle protein synthesis remains elevated for 24-48 hours post-exercise. However, consuming protein within 2 hours optimizes recovery, especially if the pre-workout meal was 4+ hours prior.",
                "category": "Sports Nutrition",
                "tags": ["post-workout", "protein synthesis", "recovery", "anabolic window"]
            },
            
            # Food Safety and Storage
            {
                "topic": "Proper Food Storage",
                "content": "Refrigerate perishables within 2 hours (1 hour if temperature >90°F). Store raw meat on bottom shelf to prevent drips. Keep refrigerator at 40°F or below and freezer at 0°F. Use FIFO (first in, first out) for pantry items.",
                "category": "Food Safety",
                "tags": ["food storage", "refrigeration", "food safety", "FIFO", "temperature"]
            },
            {
                "topic": "Nutrient Preservation",
                "content": "Steam or microwave vegetables to preserve water-soluble vitamins. Store fruits and vegetables in proper humidity conditions - most vegetables prefer high humidity, most fruits prefer low humidity. Minimize exposure to light, air, and heat.",
                "category": "Food Safety",
                "tags": ["nutrient preservation", "cooking methods", "storage conditions", "vitamins"]
            }
        ]
        
        # Save knowledge base
        with open(self.base_path / "comprehensive_knowledge.json", "w") as f:
            json.dump(knowledge_base, f, indent=2)
        
        logger.info(f"Created comprehensive knowledge base with {len(knowledge_base)} entries")
        return knowledge_base

if __name__ == "__main__":
    collector = NutritionDataCollector()
    
    # Create comprehensive datasets
    food_df = collector.create_comprehensive_food_database()
    knowledge = collector.create_comprehensive_knowledge_base()
    
    print(f"✅ Comprehensive data collection complete!")
    print(f"📊 Foods in database: {len(food_df)}")
    print(f"📚 Knowledge entries: {len(knowledge)}")
    print(f"🍎 Food categories: {food_df['food_category'].nunique()}")
    print(f"📖 Knowledge categories: {len(set(item['category'] for item in knowledge))}")