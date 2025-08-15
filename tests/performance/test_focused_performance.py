"""
Focused Performance Metrics for Nutrition Tutor Bot
Measures key performance indicators with proper error handling
"""

import time
import statistics
import json
from pathlib import Path
from typing import Dict, List
import sys

# Add src path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root / 'src'))

class FocusedPerformanceMetrics:
    """Focused performance testing with proper error handling"""
    
    def __init__(self):
        self.results = {}
        
        # Change to src directory for database access
        import os
        os.chdir(project_root / 'src')
    
    def test_vector_search_performance(self) -> Dict:
        """Test vector search performance with your actual database"""
        print("🔍 Testing Vector Search Performance...")
        
        try:
            from models.vector_store import VectorStoreManager
            
            vs = VectorStoreManager(use_local_embeddings=True)
            
            # Ensure database is loaded
            stats = vs.get_collection_stats()
            total_docs = stats.get('total_documents', 0)
            
            if total_docs == 0:
                print("   ⚠️ Database empty, initializing...")
                success = vs.load_and_embed_documents()
                if success:
                    stats = vs.get_collection_stats()
                    total_docs = stats.get('total_documents', 0)
                    print(f"   ✅ Database loaded with {total_docs} documents")
                else:
                    print("   ❌ Could not load database")
                    return {}
            
            # Test queries
            test_queries = [
                "high protein foods",
                "vitamin C sources",
                "weight loss nutrition",
                "muscle building diet",
                "healthy breakfast ideas"
            ]
            
            search_times = []
            result_counts = []
            relevance_scores = []
            
            for query in test_queries:
                start_time = time.perf_counter()
                results = vs.similarity_search(query, n_results=5)
                search_time = time.perf_counter() - start_time
                
                search_times.append(search_time)
                result_counts.append(len(results))
                
                if results:
                    avg_similarity = statistics.mean([r['similarity'] for r in results])
                    relevance_scores.append(avg_similarity)
                    print(f"   🔍 '{query}': {search_time:.3f}s, {len(results)} results, {avg_similarity:.3f} relevance")
            
            metrics = {
                'database_size': total_docs,
                'avg_search_time_ms': statistics.mean(search_times) * 1000,
                'max_search_time_ms': max(search_times) * 1000,
                'min_search_time_ms': min(search_times) * 1000,
                'avg_results_returned': statistics.mean(result_counts),
                'avg_relevance_score': statistics.mean(relevance_scores) if relevance_scores else 0,
                'total_queries_tested': len(test_queries)
            }
            
            self.results['vector_search'] = metrics
            
            print(f"\n   📊 Summary:")
            print(f"   📚 Database: {total_docs} documents")
            print(f"   ⚡ Avg search: {metrics['avg_search_time_ms']:.1f}ms")
            print(f"   🎯 Avg relevance: {metrics['avg_relevance_score']:.3f}")
            
            return metrics
            
        except Exception as e:
            print(f"   ❌ Vector search test error: {e}")
            return {}
    
    def test_rag_pipeline_performance(self) -> Dict:
        """Test RAG pipeline with realistic queries"""
        print("\n🤖 Testing RAG Pipeline Performance...")
        
        try:
            from models.rag_engine import RAGQueryEngine
            
            rag = RAGQueryEngine(use_local_embeddings=True)
            
            test_cases = [
                {
                    "query": "What are the best protein sources for muscle building?",
                    "style": "brief",
                    "expected_keywords": ["protein", "muscle", "building"]
                },
                {
                    "query": "I need vitamin C rich foods for immune support",
                    "style": "comprehensive", 
                    "expected_keywords": ["vitamin C", "immune", "citrus"]
                },
                {
                    "query": "Help me plan a 400 calorie breakfast for weight loss",
                    "style": "detailed",
                    "expected_keywords": ["breakfast", "weight loss", "calories"]
                }
            ]
            
            response_times = []
            source_counts = []
            quality_scores = []
            
            for test_case in test_cases:
                query = test_case["query"]
                style = test_case["style"]
                keywords = test_case["expected_keywords"]
                
                start_time = time.perf_counter()
                response = rag.generate_response(query, response_style=style)
                response_time = time.perf_counter() - start_time
                
                response_times.append(response_time)
                
                # Count sources used
                sources_used = len(response.get('sources', []))
                source_counts.append(sources_used)
                
                # Calculate quality score (keyword presence)
                response_text = response.get('response', '').lower()
                keyword_matches = sum(1 for keyword in keywords if keyword.lower() in response_text)
                quality_score = keyword_matches / len(keywords)
                quality_scores.append(quality_score)
                
                print(f"   💬 '{query[:30]}...': {response_time:.3f}s, {sources_used} sources, {quality_score:.3f} quality")
            
            metrics = {
                'avg_response_time_s': statistics.mean(response_times),
                'max_response_time_s': max(response_times),
                'min_response_time_s': min(response_times),
                'avg_sources_used': statistics.mean(source_counts),
                'avg_quality_score': statistics.mean(quality_scores),
                'response_styles_tested': len(set(tc['style'] for tc in test_cases)),
                'total_queries_tested': len(test_cases)
            }
            
            self.results['rag_pipeline'] = metrics
            
            print(f"\n   📊 Summary:")
            print(f"   ⚡ Avg response: {metrics['avg_response_time_s']:.3f}s")
            print(f"   📚 Avg sources: {metrics['avg_sources_used']:.1f}")
            print(f"   🎯 Quality score: {metrics['avg_quality_score']:.3f}")
            
            return metrics
            
        except Exception as e:
            print(f"   ❌ RAG pipeline test error: {e}")
            return {}
    
    def test_system_reliability(self) -> Dict:
        """Test system reliability and error handling"""
        print("\n🛡️ Testing System Reliability...")
        
        reliability_metrics = {
            'error_handling_tests': 0,
            'passed_error_tests': 0,
            'graceful_fallbacks': 0
        }
        
        # Test 1: Vector search with empty query
        try:
            from models.vector_store import VectorStoreManager
            vs = VectorStoreManager(use_local_embeddings=True)
            
            results = vs.similarity_search("", n_results=5)
            reliability_metrics['error_handling_tests'] += 1
            if isinstance(results, list):
                reliability_metrics['passed_error_tests'] += 1
                reliability_metrics['graceful_fallbacks'] += 1
            
        except Exception:
            reliability_metrics['error_handling_tests'] += 1
        
        # Test 2: RAG with invalid query
        try:
            from models.rag_engine import RAGQueryEngine
            rag = RAGQueryEngine(use_local_embeddings=True)
            
            response = rag.generate_response("", response_style="brief")
            reliability_metrics['error_handling_tests'] += 1
            if 'response' in response:
                reliability_metrics['passed_error_tests'] += 1
            
        except Exception:
            reliability_metrics['error_handling_tests'] += 1
        
        # Test 3: Nutrition API with invalid input
        try:
            from models.nutrition_api import USDANutritionAPI
            api = USDANutritionAPI()
            
            results = api.search_foods("", max_results=1)
            reliability_metrics['error_handling_tests'] += 1
            if isinstance(results, list):
                reliability_metrics['passed_error_tests'] += 1
                reliability_metrics['graceful_fallbacks'] += 1
                
        except Exception:
            reliability_metrics['error_handling_tests'] += 1
        
        # Calculate reliability score
        reliability_score = reliability_metrics['passed_error_tests'] / max(reliability_metrics['error_handling_tests'], 1)
        reliability_metrics['reliability_score'] = reliability_score
        
        self.results['system_reliability'] = reliability_metrics
        
        print(f"   📊 Error handling tests: {reliability_metrics['error_handling_tests']}")
        print(f"   ✅ Passed tests: {reliability_metrics['passed_error_tests']}")
        print(f"   🛡️ Reliability score: {reliability_score:.3f}")
        
        return reliability_metrics
    
    def generate_final_report(self) -> Dict:
        """Generate comprehensive performance report"""
        print("\n📋 Generating Final Performance Report...")
        print("=" * 60)
        
        # Run all tests
        vector_metrics = self.test_vector_search_performance()
        rag_metrics = self.test_rag_pipeline_performance()
        reliability_metrics = self.test_system_reliability()
        
        # Compile final report
        final_report = {
            'test_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'system_overview': {
                'database_documents': vector_metrics.get('database_size', 0),
                'avg_response_time_seconds': rag_metrics.get('avg_response_time_s', 0),
                'system_reliability_score': reliability_metrics.get('reliability_score', 0)
            },
            'performance_breakdown': {
                'vector_search': vector_metrics,
                'rag_pipeline': rag_metrics,
                'system_reliability': reliability_metrics
            },
            'benchmarks': {
                'vector_search_target': '< 100ms',
                'rag_response_target': '< 10s',
                'reliability_target': '> 0.8'
            }
        }
        
        # Save detailed report
        report_path = project_root / 'data' / 'performance_report.json'
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(final_report, f, indent=2)
        
        # Print summary
        print(f"\n🎯 FINAL PERFORMANCE SUMMARY:")
        print(f"   📚 Database Size: {final_report['system_overview']['database_documents']} documents")
        print(f"   ⚡ Avg Response Time: {final_report['system_overview']['avg_response_time_seconds']:.3f}s")
        print(f"   🛡️ Reliability Score: {final_report['system_overview']['system_reliability_score']:.3f}")
        print(f"   📄 Report saved: {report_path}")
        
        return final_report

if __name__ == "__main__":
    metrics = FocusedPerformanceMetrics()
    report = metrics.generate_final_report()
    
    print("\n✅ Performance testing completed!")
    print("📊 Use this data for your assignment documentation!")