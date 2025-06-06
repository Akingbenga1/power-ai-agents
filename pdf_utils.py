import os
import uuid
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

class PDFCreator:
    def __init__(self, output_dir="./"):
        """
        Initialize PDF Creator
        
        Args:
            output_dir: Directory to save PDF files (default: current directory)
        """
        self.output_dir = output_dir
        self.styles = getSampleStyleSheet()
        
        # Create custom styles
        self.custom_styles = {
            'CustomTitle': ParagraphStyle(
                'CustomTitle',
                parent=self.styles['Title'],
                fontSize=24,
                spaceAfter=30,
                alignment=TA_CENTER,
                textColor=colors.darkblue
            ),
            'CustomHeading': ParagraphStyle(
                'CustomHeading',
                parent=self.styles['Heading1'],
                fontSize=16,
                spaceAfter=12,
                spaceBefore=20,
                textColor=colors.darkblue
            ),
            'CustomBody': ParagraphStyle(
                'CustomBody',
                parent=self.styles['Normal'],
                fontSize=11,
                spaceAfter=12,
                alignment=TA_JUSTIFY,
                leftIndent=0,
                rightIndent=0
            )
        }

    def create_pdf(self, title, content, filename=None):
        """
        Create a PDF document with the given title and content
        
        Args:
            title: Document title
            content: Document content (can be string or list of paragraphs)
            filename: Optional filename (auto-generated if not provided)
            
        Returns:
            Full path to the created PDF file
        """
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')[:30]  # Limit length
            filename = f"{safe_title}_{timestamp}.pdf"
        
        # Ensure filename ends with .pdf
        if not filename.endswith('.pdf'):
            filename += '.pdf'
        
        # Create full file path
        file_path = os.path.join(self.output_dir, filename)
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            file_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build the document content
        story = []
        
        # Add title
        story.append(Paragraph(title, self.custom_styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Add content
        if isinstance(content, str):
            # Split content into paragraphs
            paragraphs = content.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    # Check if it's a heading (starts with #)
                    if para.strip().startswith('#'):
                        heading_text = para.strip().lstrip('#').strip()
                        story.append(Paragraph(heading_text, self.custom_styles['CustomHeading']))
                    else:
                        story.append(Paragraph(para.strip(), self.custom_styles['CustomBody']))
                    story.append(Spacer(1, 6))
        elif isinstance(content, list):
            # Content is already a list of paragraphs
            for item in content:
                if isinstance(item, str):
                    if item.strip().startswith('#'):
                        heading_text = item.strip().lstrip('#').strip()
                        story.append(Paragraph(heading_text, self.custom_styles['CustomHeading']))
                    else:
                        story.append(Paragraph(item, self.custom_styles['CustomBody']))
                    story.append(Spacer(1, 6))
        
        # Add footer with creation date
        story.append(Spacer(1, 30))
        footer_text = f"Document created on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        story.append(Paragraph(footer_text, footer_style))
        
        # Build the PDF
        doc.build(story)
        
        return os.path.abspath(file_path)

    def create_report_pdf(self, title, sections, filename=None):
        """
        Create a structured report PDF with multiple sections
        
        Args:
            title: Report title
            sections: List of dictionaries with 'heading' and 'content' keys
            filename: Optional filename
            
        Returns:
            Full path to the created PDF file
        """
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')[:30]
            filename = f"Report_{safe_title}_{timestamp}.pdf"
        
        # Ensure filename ends with .pdf
        if not filename.endswith('.pdf'):
            filename += '.pdf'
        
        # Create full file path
        file_path = os.path.join(self.output_dir, filename)
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            file_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build the document content
        story = []
        
        # Add title
        story.append(Paragraph(title, self.custom_styles['CustomTitle']))
        story.append(Spacer(1, 30))
        
        # Add sections
        for section in sections:
            if isinstance(section, dict) and 'heading' in section and 'content' in section:
                # Add section heading
                story.append(Paragraph(section['heading'], self.custom_styles['CustomHeading']))
                story.append(Spacer(1, 12))
                
                # Add section content
                content = section['content']
                if isinstance(content, str):
                    paragraphs = content.split('\n\n')
                    for para in paragraphs:
                        if para.strip():
                            story.append(Paragraph(para.strip(), self.custom_styles['CustomBody']))
                            story.append(Spacer(1, 6))
                elif isinstance(content, list):
                    for item in content:
                        if isinstance(item, str) and item.strip():
                            story.append(Paragraph(item.strip(), self.custom_styles['CustomBody']))
                            story.append(Spacer(1, 6))
                
                story.append(Spacer(1, 20))
        
        # Add footer with creation date
        story.append(Spacer(1, 30))
        footer_text = f"Report generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        story.append(Paragraph(footer_text, footer_style))
        
        # Build the PDF
        doc.build(story)
        
        return os.path.abspath(file_path)

def create_simple_pdf(title, content, output_dir="./", filename=None):
    """
    Convenience function to create a simple PDF
    
    Args:
        title: Document title
        content: Document content
        output_dir: Directory to save the PDF
        filename: Optional filename
        
    Returns:
        Full path to the created PDF file
    """
    creator = PDFCreator(output_dir)
    return creator.create_pdf(title, content, filename)

def create_report_pdf(title, sections, output_dir="./", filename=None):
    """
    Convenience function to create a report PDF
    
    Args:
        title: Report title
        sections: List of sections with headings and content
        output_dir: Directory to save the PDF
        filename: Optional filename
        
    Returns:
        Full path to the created PDF file
    """
    creator = PDFCreator(output_dir)
    return creator.create_report_pdf(title, sections, filename)

# Example usage
if __name__ == "__main__":
    # Test the PDF creation
    test_title = "Sample Document"
    test_content = """
    This is a sample document created using the PDF Creator utility.
    
    # Introduction
    This document demonstrates the PDF creation capabilities.
    
    # Features
    - Professional formatting
    - Custom styles
    - Automatic file naming
    - Multiple content types support
    
    # Conclusion
    The PDF Creator provides an easy way to generate professional documents.
    """
    
    pdf_path = create_simple_pdf(test_title, test_content)
    print(f"Test PDF created at: {pdf_path}") 