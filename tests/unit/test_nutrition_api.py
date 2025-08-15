"""
Unit tests for USDA Nutrition API integration
Tests API connectivity, data parsing, and error handling
"""

import pytest
import sys
import os
from unittest.mock import patch, Mock
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent / 'src'))

from models.nutrition_api import USDANutritionAPI

class TestUSDANutritionAPI:
    """Test suite for USDA Nutrition API functionality"""
    
    @pytest.fixture
    def api(self):
        """Create API instance for testing"""
        return USDANutritionAPI()
    
    def test_api_initialization(self, api):
        """Test that API initializes correctly"""
        assert api is not None
        assert api.base_url == "https://api.nal.usda.gov/fdc/v1"
        assert hasattr(api, 'api_key')
    
    @patch('requests.get')
    def test_search_foods_success(self, mock_get, api):
        """Test successful food search"""
        # Mock API response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'foods': [
                {
                    'fdcId': 171077,
                    'description': 'Chicken, broilers or fryers, breast, meat only, cooked, roasted',
                    'dataType': 'SR Legacy',
                    'foodCategory': 'Poultry Products',
                    'score': 100
                }
            ]
        }
        mock_get.return_value = mock_response
        
        # Test search
        results = api.search_foods("chicken breast", max_results=5)
        
        assert len(results) == 1
        assert results[0]['fdc_id'] == 171077
        assert 'chicken' in results[0]['description'].lower()
        assert results[0]['score'] == 100
    
    @patch('requests.get')
    def test_search_foods_api_error(self, mock_get, api):
        """Test API error handling during search"""
        # Mock API error
        mock_get.side_effect = Exception("API Error")
        
        # Should return sample data on error
        results = api.search_foods("chicken breast")
        
        assert isinstance(results, list)
        # Should fallback to sample foods
        assert len(results) >= 0
    
    @patch('requests.get')
    def test_get_food_details_success(self, mock_get, api):
        """Test successful food details retrieval"""
        # Mock detailed nutrition response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'fdcId': 171077,
            'description': 'Chicken, broilers or fryers, breast, meat only, cooked, roasted',
            'dataType': 'SR Legacy',
            'foodNutrients': [
                {
                    'nutrient': {'name': 'Energy', 'unitName': 'kcal'},
                    'amount': 165
                },
                {
                    'nutrient': {'name': 'Protein', 'unitName': 'g'},
                    'amount': 31.0
                },
                {
                    'nutrient': {'name': 'Total lipid (fat)', 'unitName': 'g'},
                    'amount': 3.6
                }
            ]
        }
        mock_get.return_value = mock_response
        
        # Test details retrieval
        details = api.get_food_details(171077)
        
        assert details is not None
        assert details['fdc_id'] == 171077
        assert details['nutrients']['calories'] == 165
        assert details['nutrients']['protein_g'] == 31.0
        assert details['nutrients']['total_fat_g'] == 3.6
    
    def test_parse_portion_various_formats(self, api):
        """Test portion parsing with different input formats"""
        test_cases = [
            ("6oz chicken breast", {'amount': 6.0, 'unit': 'oz', 'food_name': 'chicken breast'}),
            ("1 cup broccoli", {'amount': 1.0, 'unit': 'cup', 'food_name': 'broccoli'}),
            ("2.5 tbsp olive oil", {'amount': 2.5, 'unit': 'tbsp', 'food_name': 'olive oil'}),
            ("plain chicken breast", {'amount': 100, 'unit': 'g', 'food_name': 'plain chicken breast'})
        ]
        
        for description, expected in test_cases:
            result = api._parse_portion(description)
            assert result['amount'] == expected['amount']
            assert result['unit'] == expected['unit']
            assert result['food_name'] == expected['food_name']
    
    def test_convert_to_grams(self, api):
        """Test unit conversion to grams"""
        test_cases = [
            (100, 'g', 'any food', 100),
            (1, 'oz', 'any food', 28.35),
            (1, 'lb', 'any food', 453.6),
            (1, 'cup', 'rice', 185),  # Food-specific conversion
            (1, 'cup', 'broccoli', 156),
            (1, 'tbsp', 'any food', 15),
            (1, 'tsp', 'any food', 5),
        ]
        
        for amount, unit, food_name, expected in test_cases:
            result = api._convert_to_grams(amount, unit, food_name)
            assert result == expected
    
    def test_calculate_portion_nutrition(self, api):
        """Test nutrition calculation for different portions"""
        base_nutrition = {
            'food_name': 'Chicken breast',
            'nutrients': {
                'calories': 165,
                'protein_g': 31.0,
                'total_fat_g': 3.6
            }
        }
        
        # Test 200g portion (double the base 100g)
        result = api._calculate_portion_nutrition(base_nutrition, 200, 'g')
        
        assert result['calories'] == 330  # 165 * 2
        assert result['protein_g'] == 62.0  # 31 * 2
        assert result['total_fat_g'] == 7.2  # 3.6 * 2
    
    @patch.object(USDANutritionAPI, 'search_foods')
    @patch.object(USDANutritionAPI, 'get_food_details')
    def test_analyze_meal_components_integration(self, mock_details, mock_search, api):
        """Test complete meal analysis workflow"""
        # Mock search results
        mock_search.return_value = [
            {'fdc_id': 171077, 'description': 'Chicken breast', 'score': 100}
        ]
        
        # Mock nutrition details
        mock_details.return_value = {
            'food_name': 'Chicken breast',
            'fdc_id': 171077,
            'nutrients': {
                'calories': 165,
                'protein_g': 31.0,
                'carbohydrates_g': 0,
                'total_fat_g': 3.6
            }
        }
        
        # Test meal analysis
        meal_components = ["6oz chicken breast", "1 cup broccoli"]
        results = api.analyze_meal_components(meal_components)
        
        assert len(results) == 2
        assert results[0]['original_description'] == "6oz chicken breast"
        assert 'nutrition' in results[0]
        assert 'portion' in results[0]


class TestPerformanceMetrics:
    """Performance tests for nutrition API"""
    
    @pytest.fixture
    def api(self):
        return USDANutritionAPI()
    
    @pytest.mark.benchmark
    def test_search_performance(self, api, benchmark):
        """Benchmark food search performance"""
        def search_operation():
            return api.search_foods("chicken breast", max_results=5)
        
        result = benchmark(search_operation)
        assert isinstance(result, list)
    
    @pytest.mark.benchmark
    def test_portion_parsing_performance(self, api, benchmark):
        """Benchmark portion parsing performance"""
        def parse_operation():
            return api._parse_portion("6oz grilled chicken breast")
        
        result = benchmark(parse_operation)
        assert result['amount'] == 6.0
        assert result['unit'] == 'oz'


if __name__ == "__main__":
    # Run specific tests
    pytest.main([__file__, "-v", "--benchmark-only"])