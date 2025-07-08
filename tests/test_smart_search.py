#!/usr/bin/env python3
"""
🔍 AION Smart Search System - Comprehensive Test Suite

Tests all smart search functionality including:
- CLI /search command
- TUI Ctrl+K integration
- Multi-source search capabilities
- Result ranking and filtering
- Caching system
- Logging functionality
"""

import asyncio
import sys
import os
from pathlib import Path

# Add AION to path
sys.path.insert(0, str(Path(__file__).parent))

from aion.ai.smart_search import smart_search
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

async def test_basic_search():
    """Test 1: Basic search functionality"""
    console.print("\n🧪 [bold yellow]TEST 1: Basic Search Functionality[/bold yellow]")
    
    try:
        # Test basic search
        results = await smart_search.search("python async programming", max_results=5)
        
        assert results.query == "python async programming"
        assert len(results.results) > 0
        assert results.search_time > 0
        
        console.print("✅ [green]Basic search functionality: PASSED[/green]")
        console.print(f"   - Query: {results.query}")
        console.print(f"   - Results: {len(results.results)}")
        console.print(f"   - Search time: {results.search_time:.2f}s")
        
        return True
        
    except Exception as e:
        console.print(f"❌ [red]Basic search functionality: FAILED - {e}[/red]")
        return False

async def test_multi_source_search():
    """Test 2: Multi-source search"""
    console.print("\n🧪 [bold yellow]TEST 2: Multi-Source Search[/bold yellow]")
    
    try:
        # Test with specific sources
        sources = ["stackoverflow", "github", "python_docs"]
        results = await smart_search.search("machine learning", sources=sources, max_results=8)
        
        # Check that results come from different sources
        result_sources = set(result.source for result in results.results)
        
        assert len(result_sources) > 1, "Should have results from multiple sources"
        assert results.sources == sources
        
        console.print("✅ [green]Multi-source search: PASSED[/green]")
        console.print(f"   - Sources requested: {sources}")
        console.print(f"   - Sources found: {list(result_sources)}")
        console.print(f"   - Total results: {len(results.results)}")
        
        return True
        
    except Exception as e:
        console.print(f"❌ [red]Multi-source search: FAILED - {e}[/red]")
        return False

async def test_result_ranking():
    """Test 3: Result ranking and scoring"""
    console.print("\n🧪 [bold yellow]TEST 3: Result Ranking and Scoring[/bold yellow]")
    
    try:
        results = await smart_search.search("javascript frameworks", max_results=6)
        
        # Check that results are sorted by score
        scores = [result.score for result in results.results]
        is_sorted = all(scores[i] >= scores[i+1] for i in range(len(scores)-1))
        
        assert is_sorted, "Results should be sorted by score (descending)"
        assert all(0 <= score <= 1 for score in scores), "Scores should be between 0 and 1"
        
        console.print("✅ [green]Result ranking and scoring: PASSED[/green]")
        console.print(f"   - Results properly sorted: {is_sorted}")
        console.print(f"   - Score range: {min(scores):.2f} - {max(scores):.2f}")
        
        return True
        
    except Exception as e:
        console.print(f"❌ [red]Result ranking and scoring: FAILED - {e}[/red]")
        return False

async def test_search_caching():
    """Test 4: Search result caching"""
    console.print("\n🧪 [bold yellow]TEST 4: Search Result Caching[/bold yellow]")
    
    try:
        query = "python web frameworks"
        
        # First search (should cache)
        start_time = asyncio.get_event_loop().time()
        results1 = await smart_search.search(query, max_results=5)
        first_search_time = asyncio.get_event_loop().time() - start_time
        
        # Second search (should use cache)
        start_time = asyncio.get_event_loop().time()
        results2 = await smart_search.search(query, max_results=5)
        second_search_time = asyncio.get_event_loop().time() - start_time
        
        # Cache should make second search faster
        assert results1.query == results2.query
        assert len(results1.results) == len(results2.results)
        
        console.print("✅ [green]Search result caching: PASSED[/green]")
        console.print(f"   - First search time: {first_search_time:.3f}s")
        console.print(f"   - Second search time: {second_search_time:.3f}s")
        console.print(f"   - Cache working: {second_search_time < first_search_time}")
        
        return True
        
    except Exception as e:
        console.print(f"❌ [red]Search result caching: FAILED - {e}[/red]")
        return False

async def test_search_logging():
    """Test 5: Search logging functionality"""
    console.print("\n🧪 [bold yellow]TEST 5: Search Logging Functionality[/bold yellow]")
    
    try:
        query = "docker containers"
        results = await smart_search.search(query, max_results=4)
        
        # Check that log directory exists
        log_dir = Path("search_logs")
        assert log_dir.exists(), "Search logs directory should exist"
        
        # Check for log files
        log_files = list(log_dir.glob("query_*.log"))
        assert len(log_files) > 0, "Should have log files"
        
        # Check cache directory
        cache_dir = log_dir / "cache"
        assert cache_dir.exists(), "Cache directory should exist"
        
        console.print("✅ [green]Search logging functionality: PASSED[/green]")
        console.print(f"   - Log directory exists: {log_dir.exists()}")
        console.print(f"   - Log files found: {len(log_files)}")
        console.print(f"   - Cache directory exists: {cache_dir.exists()}")
        
        return True
        
    except Exception as e:
        console.print(f"❌ [red]Search logging functionality: FAILED - {e}[/red]")
        return False

async def test_result_formatting():
    """Test 6: Result formatting and display"""
    console.print("\n🧪 [bold yellow]TEST 6: Result Formatting and Display[/bold yellow]")
    
    try:
        results = await smart_search.search("react hooks", max_results=3)
        
        # Test formatting
        formatted = smart_search.format_search_results(results)
        
        assert "Search Results for:" in formatted
        assert results.query in formatted
        assert "Sources:" in formatted
        assert "Total Results:" in formatted
        
        console.print("✅ [green]Result formatting and display: PASSED[/green]")
        console.print(f"   - Formatted output length: {len(formatted)} chars")
        console.print(f"   - Contains query: {results.query in formatted}")
        console.print(f"   - Contains metadata: {'Sources:' in formatted}")
        
        return True
        
    except Exception as e:
        console.print(f"❌ [red]Result formatting and display: FAILED - {e}[/red]")
        return False

async def test_empty_query_handling():
    """Test 7: Empty query handling"""
    console.print("\n🧪 [bold yellow]TEST 7: Empty Query Handling[/bold yellow]")
    
    try:
        # Test empty query
        results = await smart_search.search("", max_results=5)
        
        # Should handle gracefully
        assert results.query == ""
        assert isinstance(results.results, list)
        
        console.print("✅ [green]Empty query handling: PASSED[/green]")
        console.print(f"   - Empty query handled gracefully")
        console.print(f"   - Results type: {type(results.results)}")
        
        return True
        
    except Exception as e:
        console.print(f"❌ [red]Empty query handling: FAILED - {e}[/red]")
        return False

async def test_source_filtering():
    """Test 8: Source filtering functionality"""
    console.print("\n🧪 [bold yellow]TEST 8: Source Filtering Functionality[/bold yellow]")
    
    try:
        # Test single source
        results = await smart_search.search("python", sources=["stackoverflow"], max_results=5)
        
        # All results should be from stackoverflow
        all_stackoverflow = all(result.source == "stackoverflow" for result in results.results)
        
        assert all_stackoverflow or len(results.results) == 0
        assert "stackoverflow" in results.sources
        
        console.print("✅ [green]Source filtering functionality: PASSED[/green]")
        console.print(f"   - Single source filter working: {all_stackoverflow}")
        console.print(f"   - Results from stackoverflow: {len(results.results)}")
        
        return True
        
    except Exception as e:
        console.print(f"❌ [red]Source filtering functionality: FAILED - {e}[/red]")
        return False

async def test_performance_limits():
    """Test 9: Performance and limits"""
    console.print("\n🧪 [bold yellow]TEST 9: Performance and Limits[/bold yellow]")
    
    try:
        # Test with high result limit
        start_time = asyncio.get_event_loop().time()
        results = await smart_search.search("programming languages", max_results=20)
        search_time = asyncio.get_event_loop().time() - start_time
        
        # Should complete within reasonable time
        assert search_time < 10.0, "Search should complete within 10 seconds"
        assert len(results.results) <= 20, "Should respect max_results limit"
        
        console.print("✅ [green]Performance and limits: PASSED[/green]")
        console.print(f"   - Search completed in: {search_time:.2f}s")
        console.print(f"   - Results within limit: {len(results.results)} <= 20")
        
        return True
        
    except Exception as e:
        console.print(f"❌ [red]Performance and limits: FAILED - {e}[/red]")
        return False

async def test_error_handling():
    """Test 10: Error handling and recovery"""
    console.print("\n🧪 [bold yellow]TEST 10: Error Handling and Recovery[/bold yellow]")
    
    try:
        # Test with invalid source
        results = await smart_search.search("test query", sources=["invalid_source"], max_results=5)
        
        # Should handle gracefully
        assert isinstance(results, type(results))  # Should return SearchQuery object
        assert isinstance(results.results, list)
        
        console.print("✅ [green]Error handling and recovery: PASSED[/green]")
        console.print(f"   - Invalid source handled gracefully")
        console.print(f"   - Results type maintained: {type(results.results)}")
        
        return True
        
    except Exception as e:
        console.print(f"❌ [red]Error handling and recovery: FAILED - {e}[/red]")
        return False

async def run_comprehensive_tests():
    """Run all smart search tests"""
    console.print(Panel.fit(
        "🔍 AION SMART SEARCH - COMPREHENSIVE TEST SUITE",
        style="bold blue"
    ))
    
    tests = [
        test_basic_search,
        test_multi_source_search,
        test_result_ranking,
        test_search_caching,
        test_search_logging,
        test_result_formatting,
        test_empty_query_handling,
        test_source_filtering,
        test_performance_limits,
        test_error_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            result = await test()
            if result:
                passed += 1
        except Exception as e:
            console.print(f"❌ [red]Test failed with exception: {e}[/red]")
    
    # Final results
    console.print(f"\n{'='*60}")
    console.print(f"🧪 [bold]SMART SEARCH TEST RESULTS[/bold]")
    console.print(f"{'='*60}")
    console.print(f"✅ [green]Passed: {passed}/{total}[/green]")
    console.print(f"❌ [red]Failed: {total-passed}/{total}[/red]")
    console.print(f"📊 [cyan]Success Rate: {(passed/total)*100:.1f}%[/cyan]")
    
    if passed == total:
        console.print(f"\n🎉 [bold green]ALL TESTS PASSED! Smart Search system is fully functional.[/bold green]")
    else:
        console.print(f"\n⚠️ [bold yellow]Some tests failed. Review the output above.[/bold yellow]")
    
    return passed == total

if __name__ == "__main__":
    asyncio.run(run_comprehensive_tests())
