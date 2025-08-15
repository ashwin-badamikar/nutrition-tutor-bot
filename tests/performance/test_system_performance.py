"""
Comprehensive Performance Metrics for Nutrition Tutor Bot
Measures response times, accuracy, and system performance
"""

import pytest
import time
import sys
import json
from pathlib import Path
from typing import Dict, List
import statistics

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / 'src'))

from models.nutrition_api import USDANutritionAPI
from models.vector_store import VectorStoreManager
from models.rag_engine import RAGQueryEngine

class PerformanceMetrics:
    """Collect and analyze system performance metrics"""
    
    def __init__(self):
        self.metrics = {
            'api_performance': {},
            'vector_search_performance': {},
            'rag_performance': {},
            'multimodal_performance': {}
        }
    
    def test_usda_api_performance(self) -> Dict:
        """Test USDA API response times"""
        print("🧪 Testing USDA API Performance...")
        
        api = USDANutritionAPI()
        test_queries = ["chicken breast", "broccoli", "salmon", "quinoa", "apple"]
        
        search_times = []
        detail_times = []
        success_count = 0
        
        for query in test_queries:
            try:
                # Test search performance
                start_time = time.time()
                search_results = api.search_foods(query, max_results=3)
                search_time = time.time() - start_time
                search_times.append(search_time)
                
                if search_results:
                    # Test detail retrieval performance
                    start_time = time.time()
                    details = api.get_food_details(search_results[0]['fdc_id'])
                    detail_time = time.time() - start_time
                    detail_times.append(detail_time)
                    
                    if details:
                        success_count += 1
                
            except Exception as e:
                print(f"   ❌ Error with {query}: {e}")
        
        api_metrics = {
            'search_avg_time': statistics.mean(search_times) if search_times else 0,
            'search_max_time': max(search_times) if search_times else 0,
            'detail_avg_time': statistics.mean(detail_times) if detail_times else 0,
            'detail_max_time': max(detail_times) if detail_times else 0,
            'success_rate': success_count / len(test_queries),
            'total_queries': len(test_queries)
        }
        
        self.metrics['api_performance'] = api_metrics
        
        print(f"   📊 Search avg time: {api_metrics['search_avg_time']:.3f}s")
        print(f"   📊 Detail avg time: {api_metrics['detail_avg_time']:.3f}s")
        print(f"   📊 Success rate: {api_metrics['success_rate']:.1%}")
        
        return api_metrics
    
    def test_vector_search_performance(self) -> Dict:
        """Test vector database search performance"""
        print("\n🧪 Testing Vector Search Performance...")
        
        try:
            vs = VectorStoreManager(use_local_embeddings=True)
            
            test_queries = [
                "high protein foods",
                "vitamin C sources", 
                "weight loss meals",
                "post workout nutrition",
                "vegetarian protein"
            ]
            
            search_times = []
            result_counts = []
            relevance_scores = []
            
            for query in test_queries:
                start_time = time.time()
                results = vs.similarity_search(query, n_results=5)
                search_time = time.time() - start_time
                
                search_times.append(search_time)
                result_counts.append(len(results))
                
                if results:
                    # Average similarity score as relevance measure
                    avg_similarity = statistics.mean([r['similarity'] for r in results])
                    relevance_scores.append(avg_similarity)
            
            vector_metrics = {
                'avg_search_time': statistics.mean(search_times),
                'max_search_time': max(search_times),
                'avg_results_returned': statistics.mean(result_counts),
                'avg_relevance_score': statistics.mean(relevance_scores) if relevance_scores else 0,
                'total_test_queries': len(test_queries)
            }
            
            self.metrics['vector_search_performance'] = vector_metrics
            
            print(f"   📊 Avg search time: {vector_metrics['avg_search_time']:.3f}s")
            print(f"   📊 Avg results: {vector_metrics['avg_results_returned']:.1f}")
            print(f"   📊 Avg relevance: {vector_metrics['avg_relevance_score']:.3f}")
            
            return vector_metrics
            
        except Exception as e:
            print(f"   ❌ Vector search error: {e}")
            return {}
    
    def test_rag_pipeline_performance(self) -> Dict:
        """Test complete RAG pipeline performance"""
        print("\n🧪 Testing RAG Pipeline Performance...")
        
        try:
            rag = RAGQueryEngine(use_local_embeddings=True)
            
            test_queries = [
                {"query": "What are good protein sources for muscle building?", "expected_terms": ["protein", "muscle", "chicken", "salmon"]},
                {"query": "I need foods high in vitamin C", "expected_terms": ["vitamin C", "citrus", "orange", "broccoli"]},
                {"query": "Help me plan a weight loss breakfast", "expected_terms": ["weight loss", "breakfast", "calories", "protein"]}
            ]
            
            response_times = []
            context_relevance = []
            response_quality = []
            
            for test_case in test_queries:
                query = test_case["query"]
                expected_terms = test_case["expected_terms"]
                
                start_time = time.time()
                response = rag.generate_response(query, response_style="brief")
                response_time = time.time() - start_time
                
                response_times.append(response_time)
                
                # Measure context relevance
                if response.get('sources'):
                    context_relevance.append(len(response['sources']))
                
                # Simple response quality check (contains expected terms)
                response_text = response.get('response', '').lower()
                term_matches = sum(1 for term in expected_terms if term.lower() in response_text)
                quality_score = term_matches / len(expected_terms)
                response_quality.append(quality_score)
            
            rag_metrics = {
                'avg_response_time': statistics.mean(response_times),
                'max_response_time': max(response_times),
                'avg_context_sources': statistics.mean(context_relevance) if context_relevance else 0,
                'avg_quality_score': statistics.mean(response_quality) if response_quality else 0,
                'total_test_queries': len(test_queries)
            }
            
            self.metrics['rag_performance'] = rag_metrics
            
            print(f"   📊 Avg response time: {rag_metrics['avg_response_time']:.3f}s")
            print(f"   📊 Avg sources used: {rag_metrics['avg_context_sources']:.1f}")
            print(f"   📊 Quality score: {rag_metrics['avg_quality_score']:.3f}")
            
            return rag_metrics
            
        except Exception as e:
            print(f"   ❌ RAG pipeline error: {e}")
            return {}
    
    def test_database_statistics(self) -> Dict:
        """Get comprehensive database statistics"""
        print("\n🧪 Testing Database Statistics...")
        
        try:
            vs = VectorStoreManager(use_local_embeddings=True)
            stats = vs.get_collection_stats()
            
            print(f"   📊 Total documents: {stats.get('total_documents', 0)}")
            print(f"   📊 Document types: {len(stats.get('document_types', {}))}")
            print(f"   📊 Embedding model: {stats.get('embedding_model', 'Unknown')}")
            
            self.metrics['database_stats'] = stats
            return stats
            
        except Exception as e:
            print(f"   ❌ Database stats error: {e}")
            return {}
    
    def generate_performance_report(self) -> Dict:
        """Generate comprehensive performance report"""
        print("\n🔬 Generating Performance Report...")
        print("=" * 60)
        
        # Run all performance tests
        api_perf = self.test_usda_api_performance()
        vector_perf = self.test_vector_search_performance()
        rag_perf = self.test_rag_pipeline_performance()
        db_stats = self.test_database_statistics()
        
        # Compile overall metrics
        overall_metrics = {
            'system_performance': {
                'api_avg_response': api_perf.get('search_avg_time', 0),
                'vector_search_avg': vector_perf.get('avg_search_time', 0),
                'rag_pipeline_avg': rag_perf.get('avg_response_time', 0),
                'total_documents': db_stats.get('total_documents', 0)
            },
            'quality_metrics': {
                'api_success_rate': api_perf.get('success_rate', 0),
                'avg_relevance_score': vector_perf.get('avg_relevance_score', 0),
                'rag_quality_score': rag_perf.get('avg_quality_score', 0)
            },
            'detailed_metrics': self.metrics
        }
        
        # Save metrics to file
        metrics_path = Path("../data/performance_metrics.json")
        with open(metrics_path, 'w') as f:
            json.dump(overall_metrics, f, indent=2)
        
        print(f"\n📊 PERFORMANCE SUMMARY:")
        print(f"   🌐 API Response Time: {api_perf.get('search_avg_time', 0):.3f}s")
        print(f"   🔍 Vector Search Time: {vector_perf.get('avg_search_time', 0):.3f}s") 
        print(f"   🤖 RAG Pipeline Time: {rag_perf.get('avg_response_time', 0):.3f}s")
        print(f"   📚 Database Size: {db_stats.get('total_documents', 0)} documents")
        print(f"   ✅ Overall Success Rate: {api_perf.get('success_rate', 0):.1%}")
        
        print(f"\n💾 Performance metrics saved to: {metrics_path}")
        
        return overall_metrics


def run_comprehensive_performance_test():
    """Run all performance tests and generate report"""
    print("🚀 Starting Comprehensive Performance Testing...")
    print("=" * 60)
    
    metrics = PerformanceMetrics()
    report = metrics.generate_performance_report()
    
    print("\n✅ Performance testing completed!")
    return report

if __name__ == "__main__":
    run_comprehensive_performance_test()