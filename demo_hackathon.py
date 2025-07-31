#!/usr/bin/env python3
"""
🚀 HACKATHON DEMO SCRIPT
LLM-Powered Intelligent Query–Retrieval System
"""

import requests
import json
import time
from datetime import datetime

class HackathonDemo:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1"
        
    def print_header(self, title):
        print(f"\n{'='*60}")
        print(f"🎯 {title}")
        print(f"{'='*60}")
        
    def print_success(self, message):
        print(f"✅ {message}")
        
    def print_info(self, message):
        print(f"ℹ️  {message}")
        
    def demo_health_check(self):
        """Demo 1: Health Check"""
        self.print_header("HEALTH CHECK DEMO")
        
        try:
            response = requests.get(f"{self.api_url}/health")
            if response.status_code == 200:
                data = response.json()
                self.print_success("System is healthy!")
                print(f"📊 Status: {data['status']}")
                print(f"🕒 Timestamp: {data['timestamp']}")
                print(f"🏷️  System: {data['system']}")
                print(f"📦 Version: {data['version']}")
            else:
                print(f"❌ Health check failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
            
    def demo_system_info(self):
        """Demo 2: System Information"""
        self.print_header("SYSTEM INFORMATION DEMO")
        
        try:
            response = requests.get(f"{self.api_url}/system/info")
            if response.status_code == 200:
                data = response.json()
                self.print_success("System information retrieved!")
                
                print(f"🖥️  Platform: {data['system']['platform']}")
                print(f"🐍 Python: {data['system']['python_version']}")
                print(f"💾 Memory: {data['system']['memory_available']} available")
                
                print(f"\n🚀 Features ({len(data['features'])} total):")
                for feature in data['features']:
                    print(f"   • {feature}")
                    
                print(f"\n🎯 Hackathon Features:")
                for feature in data['hackathon_features']:
                    print(f"   • {feature}")
                    
            else:
                print(f"❌ System info failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
            
    def demo_query_processing(self):
        """Demo 3: Query Processing with Enhanced Features"""
        self.print_header("QUERY PROCESSING DEMO")
        
        # Test data
        test_data = {
            "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
            "questions": [
                "What is the grace period for premium payment?"
            ]
        }
        
        try:
            self.print_info("Processing insurance policy queries...")
            start_time = time.time()
            
            response = requests.post(
                f"{self.api_url}/hackrx/run",
                headers={"Content-Type": "application/json"},
                json=test_data
            )
            
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.print_success("Query processing completed!")
                
                # Display performance metrics
                print(f"⚡ Processing Time: {data['performance']['total_time']}s")
                print(f"📊 Questions/Second: {data['performance']['questions_per_second']}")
                print(f"📄 Document Pages: {data['metadata']['document_pages']}")
                print(f"🔍 Chunks Processed: {data['metadata']['chunks_processed']}")
                print(f"💾 Cached Response: {data['metadata']['cached']}")
                
                # Display answers with confidence scores
                print(f"\n🤖 AI-Generated Answers:")
                for i, answer in enumerate(data['answers'], 1):
                    print(f"\n   Q{i}: {test_data['questions'][i-1]}")
                    print(f"   💡 Answer: {answer['answer']}")
                    print(f"   🎯 Confidence: {answer['confidence']}")
                    print(f"   📍 Source: Page {answer['source']['page']}")
                    
            else:
                print(f"❌ Query processing failed: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            
    def demo_caching_feature(self):
        """Demo 4: Caching System"""
        self.print_header("CACHING SYSTEM DEMO")
        
        test_data = {
            "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
            "questions": ["What is the grace period for premium payment?"]
        }
        
        try:
            # First request (cache miss)
            self.print_info("Making first request (cache miss)...")
            start_time = time.time()
            response1 = requests.post(
                f"{self.api_url}/hackrx/run",
                headers={"Content-Type": "application/json"},
                json=test_data
            )
            first_time = time.time() - start_time
            
            # Second request (cache hit)
            self.print_info("Making second request (cache hit)...")
            start_time = time.time()
            response2 = requests.post(
                f"{self.api_url}/hackrx/run",
                headers={"Content-Type": "application/json"},
                json=test_data
            )
            second_time = time.time() - start_time
            
            if response1.status_code == 200 and response2.status_code == 200:
                data1 = response1.json()
                data2 = response2.json()
                
                self.print_success("Caching demo completed!")
                print(f"⏱️  First request: {first_time:.3f}s")
                print(f"⚡ Second request: {second_time:.3f}s")
                print(f"🚀 Speed improvement: {first_time/second_time:.1f}x faster")
                print(f"💾 Cache hit: {data2['metadata']['cached']}")
                
            else:
                print(f"❌ Caching demo failed")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            
    def run_full_demo(self):
        """Run the complete hackathon demo"""
        print(f"\n{'🚀'*20}")
        print("LLM-POWERED INTELLIGENT QUERY SYSTEM")
        print("HACKATHON DEMO")
        print(f"{'🚀'*20}")
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all demos
        self.demo_health_check()
        self.demo_system_info()
        self.demo_query_processing()
        self.demo_caching_feature()
        
        print(f"\n{'🎉'*20}")
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("Your system is ready for the hackathon!")
        print(f"{'🎉'*20}")

if __name__ == "__main__":
    demo = HackathonDemo()
    demo.run_full_demo() 