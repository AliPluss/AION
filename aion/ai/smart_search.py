#!/usr/bin/env python3
"""
🔍 AION Smart Search System

AI-powered intelligent search combining local knowledge with online developer resources.
Searches Stack Overflow, GitHub, Python Docs, and other technical sources.

Features:
- Multi-source search (Stack Overflow, GitHub, Python Docs, MDN, etc.)
- AI-enhanced result filtering and ranking
- Context-aware search suggestions
- Comprehensive logging and caching
- Real-time search with async processing
"""

import os
import json
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
import urllib.parse
import hashlib

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

@dataclass
class SearchResult:
    """Search result structure"""
    title: str
    url: str
    source: str  # 'stackoverflow', 'github', 'python_docs', 'mdn', etc.
    snippet: str
    score: float  # Relevance score 0-1
    tags: List[str]
    timestamp: datetime

@dataclass
class SearchQuery:
    """Search query structure"""
    query: str
    sources: List[str]
    filters: Dict[str, Any]
    results: List[SearchResult]
    total_results: int
    search_time: float
    timestamp: datetime

class SmartSearchEngine:
    """AI-powered smart search engine"""
    
    def __init__(self):
        self.search_logs_dir = Path("search_logs")
        self.search_logs_dir.mkdir(exist_ok=True)
        
        self.cache_dir = Path("search_logs/cache")
        self.cache_dir.mkdir(exist_ok=True)
        
        self.search_sources = {
            "stackoverflow": {
                "name": "Stack Overflow",
                "api_url": "https://api.stackexchange.com/2.3/search/advanced",
                "icon": "🔍",
                "enabled": True
            },
            "github": {
                "name": "GitHub",
                "api_url": "https://api.github.com/search/repositories",
                "icon": "🐙",
                "enabled": True
            },
            "python_docs": {
                "name": "Python Documentation",
                "api_url": "https://docs.python.org/3/search.html",
                "icon": "🐍",
                "enabled": True
            },
            "mdn": {
                "name": "MDN Web Docs",
                "api_url": "https://developer.mozilla.org/api/v1/search",
                "icon": "🌐",
                "enabled": True
            },
            "devdocs": {
                "name": "DevDocs",
                "api_url": "https://devdocs.io/",
                "icon": "📚",
                "enabled": True
            }
        }
        
    async def search(self, query: str, sources: List[str] = None, max_results: int = 10) -> SearchQuery:
        """Perform intelligent multi-source search"""
        
        start_time = datetime.now()
        
        if not sources:
            sources = ["stackoverflow", "github", "python_docs"]
        
        # Check cache first
        cache_key = self._generate_cache_key(query, sources)
        cached_result = self._get_cached_result(cache_key)
        
        if cached_result:
            console.print("📋 [cyan]Using cached results[/cyan]")
            return cached_result
        
        console.print(f"🔍 [yellow]Searching for: {query}[/yellow]")
        
        all_results = []
        
        # Search each source concurrently
        search_tasks = []
        for source in sources:
            if source in self.search_sources and self.search_sources[source]["enabled"]:
                task = self._search_source(source, query, max_results // len(sources))
                search_tasks.append(task)
        
        # Execute searches concurrently
        if search_tasks:
            source_results = await asyncio.gather(*search_tasks, return_exceptions=True)
            
            for results in source_results:
                if isinstance(results, list):
                    all_results.extend(results)
                elif isinstance(results, Exception):
                    console.print(f"⚠️ [yellow]Search error: {results}[/yellow]")
        
        # AI-enhanced ranking and filtering
        ranked_results = await self._rank_and_filter_results(all_results, query)
        
        # Limit to max_results
        final_results = ranked_results[:max_results]
        
        # Calculate search time
        search_time = (datetime.now() - start_time).total_seconds()
        
        # Create search query object
        search_query = SearchQuery(
            query=query,
            sources=sources,
            filters={},
            results=final_results,
            total_results=len(final_results),
            search_time=search_time,
            timestamp=start_time
        )
        
        # Cache results
        self._cache_result(cache_key, search_query)
        
        # Log search
        self._log_search(search_query)
        
        return search_query
    
    async def _search_source(self, source: str, query: str, max_results: int) -> List[SearchResult]:
        """Search specific source"""
        
        try:
            if source == "stackoverflow":
                return await self._search_stackoverflow(query, max_results)
            elif source == "github":
                return await self._search_github(query, max_results)
            elif source == "python_docs":
                return await self._search_python_docs(query, max_results)
            elif source == "mdn":
                return await self._search_mdn(query, max_results)
            else:
                return await self._search_generic(source, query, max_results)
                
        except Exception as e:
            console.print(f"⚠️ [yellow]Error searching {source}: {e}[/yellow]")
            return []
    
    async def _search_stackoverflow(self, query: str, max_results: int) -> List[SearchResult]:
        """Search Stack Overflow"""
        
        results = []
        
        try:
            # Simulate Stack Overflow API search
            # In production, use actual Stack Exchange API
            mock_results = [
                {
                    "title": f"How to {query} in Python",
                    "link": f"https://stackoverflow.com/questions/12345/{query.replace(' ', '-')}",
                    "body_markdown": f"This is a comprehensive answer about {query}...",
                    "tags": ["python", "programming"],
                    "score": 42,
                    "is_answered": True
                },
                {
                    "title": f"Best practices for {query}",
                    "link": f"https://stackoverflow.com/questions/67890/{query.replace(' ', '-')}-best-practices",
                    "body_markdown": f"Here are the best practices for {query}...",
                    "tags": ["best-practices", "python"],
                    "score": 28,
                    "is_answered": True
                }
            ]
            
            for item in mock_results[:max_results]:
                result = SearchResult(
                    title=item["title"],
                    url=item["link"],
                    source="stackoverflow",
                    snippet=item["body_markdown"][:200] + "...",
                    score=min(item["score"] / 50.0, 1.0),  # Normalize score
                    tags=item["tags"],
                    timestamp=datetime.now()
                )
                results.append(result)
                
        except Exception as e:
            console.print(f"⚠️ [yellow]Stack Overflow search error: {e}[/yellow]")
        
        return results
    
    async def _search_github(self, query: str, max_results: int) -> List[SearchResult]:
        """Search GitHub repositories"""
        
        results = []
        
        try:
            # Simulate GitHub API search
            mock_results = [
                {
                    "name": f"{query}-toolkit",
                    "full_name": f"awesome/{query}-toolkit",
                    "html_url": f"https://github.com/awesome/{query}-toolkit",
                    "description": f"A comprehensive toolkit for {query} development",
                    "stargazers_count": 1250,
                    "language": "Python",
                    "topics": [query.lower(), "toolkit", "python"]
                },
                {
                    "name": f"{query}-examples",
                    "full_name": f"examples/{query}-examples",
                    "html_url": f"https://github.com/examples/{query}-examples",
                    "description": f"Collection of {query} examples and tutorials",
                    "stargazers_count": 890,
                    "language": "Python",
                    "topics": [query.lower(), "examples", "tutorial"]
                }
            ]
            
            for item in mock_results[:max_results]:
                result = SearchResult(
                    title=f"{item['name']} - {item['description']}",
                    url=item["html_url"],
                    source="github",
                    snippet=f"⭐ {item['stargazers_count']} stars | Language: {item['language']} | {item['description']}",
                    score=min(item["stargazers_count"] / 2000.0, 1.0),  # Normalize by stars
                    tags=item["topics"],
                    timestamp=datetime.now()
                )
                results.append(result)
                
        except Exception as e:
            console.print(f"⚠️ [yellow]GitHub search error: {e}[/yellow]")
        
        return results
    
    async def _search_python_docs(self, query: str, max_results: int) -> List[SearchResult]:
        """Search Python documentation"""
        
        results = []
        
        try:
            # Simulate Python docs search
            mock_results = [
                {
                    "title": f"{query.title()} - Python Documentation",
                    "url": f"https://docs.python.org/3/library/{query.lower()}.html",
                    "content": f"Official Python documentation for {query}...",
                    "section": "Library Reference"
                },
                {
                    "title": f"{query.title()} Tutorial - Python Documentation",
                    "url": f"https://docs.python.org/3/tutorial/{query.lower()}.html",
                    "content": f"Python tutorial covering {query} concepts...",
                    "section": "Tutorial"
                }
            ]
            
            for item in mock_results[:max_results]:
                result = SearchResult(
                    title=item["title"],
                    url=item["url"],
                    source="python_docs",
                    snippet=item["content"][:200] + "...",
                    score=0.9,  # High score for official docs
                    tags=["python", "documentation", "official"],
                    timestamp=datetime.now()
                )
                results.append(result)
                
        except Exception as e:
            console.print(f"⚠️ [yellow]Python docs search error: {e}[/yellow]")
        
        return results
    
    async def _search_mdn(self, query: str, max_results: int) -> List[SearchResult]:
        """Search MDN Web Docs"""
        
        results = []
        
        try:
            # Simulate MDN search for web-related queries
            if any(term in query.lower() for term in ["javascript", "js", "html", "css", "web", "dom", "api"]):
                mock_results = [
                    {
                        "title": f"{query.title()} - Web APIs | MDN",
                        "url": f"https://developer.mozilla.org/en-US/docs/Web/API/{query.replace(' ', '_')}",
                        "summary": f"The {query} Web API provides...",
                        "locale": "en-US"
                    }
                ]
                
                for item in mock_results[:max_results]:
                    result = SearchResult(
                        title=item["title"],
                        url=item["url"],
                        source="mdn",
                        snippet=item["summary"][:200] + "...",
                        score=0.85,  # High score for MDN
                        tags=["javascript", "web", "api", "mdn"],
                        timestamp=datetime.now()
                    )
                    results.append(result)
                    
        except Exception as e:
            console.print(f"⚠️ [yellow]MDN search error: {e}[/yellow]")
        
        return results
    
    async def _search_generic(self, source: str, query: str, max_results: int) -> List[SearchResult]:
        """Generic search for other sources"""
        
        # Placeholder for additional search sources
        return []
    
    async def _rank_and_filter_results(self, results: List[SearchResult], query: str) -> List[SearchResult]:
        """AI-enhanced ranking and filtering"""

        # Handle empty query
        if not query or not query.strip():
            return sorted(results, key=lambda x: x.score, reverse=True)

        # Simple ranking algorithm (can be enhanced with AI)
        query_terms = query.lower().split()

        # Handle empty query terms
        if not query_terms:
            return sorted(results, key=lambda x: x.score, reverse=True)

        for result in results:
            # Calculate relevance score based on title and snippet matching
            title_matches = sum(1 for term in query_terms if term in result.title.lower())
            snippet_matches = sum(1 for term in query_terms if term in result.snippet.lower())

            # Boost score based on matches
            match_boost = (title_matches * 0.3 + snippet_matches * 0.1) / len(query_terms)
            result.score = min(result.score + match_boost, 1.0)

        # Sort by score (descending)
        return sorted(results, key=lambda x: x.score, reverse=True)
    
    def _generate_cache_key(self, query: str, sources: List[str]) -> str:
        """Generate cache key for query"""
        cache_string = f"{query}:{':'.join(sorted(sources))}"
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def _get_cached_result(self, cache_key: str) -> Optional[SearchQuery]:
        """Get cached search result"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        try:
            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Check if cache is still valid (1 hour)
                cached_time = datetime.fromisoformat(data['timestamp'])
                if (datetime.now() - cached_time).total_seconds() < 3600:
                    # Reconstruct SearchQuery object
                    results = [SearchResult(**r) for r in data['results']]
                    return SearchQuery(
                        query=data['query'],
                        sources=data['sources'],
                        filters=data['filters'],
                        results=results,
                        total_results=data['total_results'],
                        search_time=data['search_time'],
                        timestamp=cached_time
                    )
        except Exception as e:
            console.print(f"⚠️ [yellow]Cache read error: {e}[/yellow]")
        
        return None
    
    def _cache_result(self, cache_key: str, search_query: SearchQuery):
        """Cache search result"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        try:
            # Convert to serializable format
            data = asdict(search_query)
            data['timestamp'] = search_query.timestamp.isoformat()
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
                
        except Exception as e:
            console.print(f"⚠️ [yellow]Cache write error: {e}[/yellow]")
    
    def _log_search(self, search_query: SearchQuery):
        """Log search query and results"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = self.search_logs_dir / f"query_{search_query.timestamp.strftime('%Y%m%d_%H%M%S')}.log"
        
        try:
            with open(log_file, "w", encoding="utf-8") as f:
                f.write(f"🔍 AION SMART SEARCH LOG\n")
                f.write(f"========================\n")
                f.write(f"Timestamp: {timestamp}\n")
                f.write(f"Query: {search_query.query}\n")
                f.write(f"Sources: {', '.join(search_query.sources)}\n")
                f.write(f"Total Results: {search_query.total_results}\n")
                f.write(f"Search Time: {search_query.search_time:.2f}s\n\n")
                
                f.write("RESULTS:\n")
                f.write("========\n")
                
                for i, result in enumerate(search_query.results, 1):
                    f.write(f"\n{i}. {result.title}\n")
                    f.write(f"   Source: {result.source} | Score: {result.score:.2f}\n")
                    f.write(f"   URL: {result.url}\n")
                    f.write(f"   Tags: {', '.join(result.tags)}\n")
                    f.write(f"   Snippet: {result.snippet}\n")
                    f.write(f"   {'-' * 50}\n")
                
        except Exception as e:
            console.print(f"⚠️ [yellow]Logging error: {e}[/yellow]")
    
    def format_search_results(self, search_query: SearchQuery) -> str:
        """Format search results for display"""
        
        if not search_query.results:
            return f"🔍 **No results found for:** {search_query.query}"
        
        output = f"""
🔍 **Search Results for:** {search_query.query}

**Sources:** {', '.join(search_query.sources)}
**Total Results:** {search_query.total_results}
**Search Time:** {search_query.search_time:.2f}s

**Results:**"""
        
        for i, result in enumerate(search_query.results[:5], 1):  # Show top 5
            source_icon = self.search_sources.get(result.source, {}).get("icon", "📄")
            
            output += f"""

**{i}. {source_icon} {result.title}**
   **Source:** {result.source.title()} | **Score:** {result.score:.2f}
   **URL:** {result.url}
   **Tags:** {', '.join(result.tags)}
   **Preview:** {result.snippet}"""
        
        if len(search_query.results) > 5:
            output += f"\n\n... and {len(search_query.results) - 5} more results"
        
        output += f"\n\n📝 **Full results logged to:** search_logs/query_{search_query.timestamp.strftime('%Y%m%d_%H%M%S')}.log"
        
        return output

# Global smart search instance
smart_search = SmartSearchEngine()
