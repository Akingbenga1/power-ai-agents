import os
import re
from datetime import datetime
from pdf_utils import create_simple_pdf, create_report_pdf

class PDFAgentTools:
    """
    Tools for the PDF Producer agent to create actual PDF files
    """
    
    def __init__(self, output_dir="./"):
        self.output_dir = output_dir
        
    def create_pdf_from_text(self, user_request):
        """
        Create a PDF from a user's text request
        
        Args:
            user_request: The user's request containing title and content
            
        Returns:
            Dictionary with file path, summary, and details
        """
        try:
            # Extract title and content from the request
            title, content = self._parse_user_request(user_request)
            
            # Create the PDF
            file_path = create_simple_pdf(
                title=title,
                content=content,
                output_dir=self.output_dir
            )
            
            # Generate summary and details
            word_count = len(content.split())
            paragraph_count = len([p for p in content.split('\n\n') if p.strip()])
            
            return {
                'success': True,
                'file_path': file_path,
                'title': title,
                'summary': f"Created PDF document with {word_count} words and {paragraph_count} paragraphs",
                'details': {
                    'word_count': word_count,
                    'paragraph_count': paragraph_count,
                    'file_size': self._get_file_size(file_path),
                    'creation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'file_path': None
            }
    
    def create_report_pdf_from_sections(self, title, sections_data):
        """
        Create a structured report PDF from sections
        
        Args:
            title: Report title
            sections_data: List of sections or string to parse into sections
            
        Returns:
            Dictionary with file path, summary, and details
        """
        try:
            # Parse sections if needed
            if isinstance(sections_data, str):
                sections = self._parse_sections_from_text(sections_data)
            else:
                sections = sections_data
            
            # Create the PDF
            file_path = create_report_pdf(
                title=title,
                sections=sections,
                output_dir=self.output_dir
            )
            
            # Generate summary and details
            total_words = sum(len(section.get('content', '').split()) for section in sections)
            section_count = len(sections)
            
            return {
                'success': True,
                'file_path': file_path,
                'title': title,
                'summary': f"Created report PDF with {section_count} sections and {total_words} total words",
                'details': {
                    'section_count': section_count,
                    'total_words': total_words,
                    'file_size': self._get_file_size(file_path),
                    'creation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'file_path': None
            }
    
    def _parse_user_request(self, user_request):
        """
        Parse user request to extract title and content
        """
        # Look for explicit title indicators
        title_patterns = [
            r'title[:\s]+([^\n]+)',
            r'create.*pdf.*["\']([^"\']+)["\']',
            r'document.*["\']([^"\']+)["\']',
            r'report.*["\']([^"\']+)["\']'
        ]
        
        title = "Document"  # Default title
        content = user_request
        
        # Try to extract title
        for pattern in title_patterns:
            match = re.search(pattern, user_request, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                # Remove the title line from content
                content = re.sub(pattern, '', user_request, flags=re.IGNORECASE).strip()
                break
        
        # If no explicit title found, try to use first line as title
        lines = user_request.strip().split('\n')
        if len(lines) > 1 and len(lines[0]) < 100:
            potential_title = lines[0].strip()
            if not potential_title.lower().startswith(('create', 'make', 'generate')):
                title = potential_title
                content = '\n'.join(lines[1:]).strip()
        
        # Clean up content
        if not content or content == title:
            content = user_request
        
        return title, content
    
    def _parse_sections_from_text(self, text):
        """
        Parse text into sections based on headings
        """
        sections = []
        
        # Split by markdown-style headings
        parts = re.split(r'\n#+\s*([^\n]+)', text)
        
        if len(parts) > 1:
            # First part might be introduction
            if parts[0].strip():
                sections.append({
                    'heading': 'Introduction',
                    'content': parts[0].strip()
                })
            
            # Process heading-content pairs
            for i in range(1, len(parts), 2):
                if i + 1 < len(parts):
                    heading = parts[i].strip()
                    content = parts[i + 1].strip()
                    sections.append({
                        'heading': heading,
                        'content': content
                    })
        else:
            # No clear sections, create a single section
            sections.append({
                'heading': 'Content',
                'content': text.strip()
            })
        
        return sections
    
    def _get_file_size(self, file_path):
        """
        Get file size in human-readable format
        """
        try:
            size_bytes = os.path.getsize(file_path)
            if size_bytes < 1024:
                return f"{size_bytes} bytes"
            elif size_bytes < 1024 * 1024:
                return f"{size_bytes / 1024:.1f} KB"
            else:
                return f"{size_bytes / (1024 * 1024):.1f} MB"
        except:
            return "Unknown"

# Global instance for the PDF Producer agent to use
pdf_tools = PDFAgentTools()

def create_pdf_document(user_request):
    """
    Main function for PDF Producer agent to create PDFs
    
    Args:
        user_request: User's request for PDF creation
        
    Returns:
        Formatted response with file path and details
    """
    result = pdf_tools.create_pdf_from_text(user_request)
    
    if result['success']:
        response = f"""✅ PDF Created Successfully!

📄 File Path: {result['file_path']}

📋 Content Summary: {result['summary']}

📊 Document Details:
   • Title: {result['title']}
   • Word Count: {result['details']['word_count']}
   • Paragraphs: {result['details']['paragraph_count']}
   • File Size: {result['details']['file_size']}
   • Created: {result['details']['creation_time']}

The PDF has been saved to your root directory and is ready to use!"""
    else:
        response = f"""❌ PDF Creation Failed!

Error: {result['error']}

Please check your request and try again."""
    
    return response

def create_report_document(title, content):
    """
    Function for creating structured report PDFs
    
    Args:
        title: Report title
        content: Report content (will be parsed into sections)
        
    Returns:
        Formatted response with file path and details
    """
    result = pdf_tools.create_report_pdf_from_sections(title, content)
    
    if result['success']:
        response = f"""✅ Report PDF Created Successfully!

📄 File Path: {result['file_path']}

📋 Content Summary: {result['summary']}

📊 Document Details:
   • Title: {result['title']}
   • Sections: {result['details']['section_count']}
   • Total Words: {result['details']['total_words']}
   • File Size: {result['details']['file_size']}
   • Created: {result['details']['creation_time']}

The report PDF has been saved to your root directory and is ready to use!"""
    else:
        response = f"""❌ Report PDF Creation Failed!

Error: {result['error']}

Please check your request and try again."""
    
    return response

# Example usage for testing
if __name__ == "__main__":
    # Test PDF creation
    test_request = """
    Title: Sample Business Report
    
    # Executive Summary
    This is a sample business report demonstrating PDF creation capabilities.
    
    # Market Analysis
    The market shows strong growth potential with increasing demand.
    
    # Recommendations
    We recommend proceeding with the proposed strategy.
    """
    
    print(create_pdf_document(test_request)) 