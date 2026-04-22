from pathlib import Path
import pdfplumber
import re
from typing import List, Tuple


def extract_uploaded_pdf_text(file_path: Path) -> str:
    """
    Extract full cleaned text from an uploaded PDF file.

    Requirements covered:
    - Handles multiple pages
    - Handles empty pages safely
    - Returns full cleaned text
    - Applies basic preprocessing (extra spaces/newlines removal)
    """
    if file_path.suffix.lower() != ".pdf":
        raise ValueError(f"Only PDF files are supported. Got: {file_path.suffix}")

    pages_text: List[str] = []

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""

                # Skip empty or whitespace-only pages safely.
                if not page_text.strip():
                    continue

                # Basic preprocessing for cleaner downstream NLP.
                page_text = page_text.replace("\r\n", "\n").replace("\r", "\n")
                page_text = re.sub(r"[ \t]+", " ", page_text)
                page_text = re.sub(r"\n{3,}", "\n\n", page_text)
                page_text = "\n".join(line.strip() for line in page_text.split("\n"))
                page_text = page_text.strip()

                if page_text:
                    pages_text.append(page_text)

        if not pages_text:
            raise ValueError("Could not extract text from PDF: no readable text found.")

        return "\n\n".join(pages_text)

    except Exception as exc:
        raise ValueError(f"Error extracting PDF text: {str(exc)}")


class TextExtractor:
    """
    Extracts and cleans text from PDF files using pdfplumber.
    
    Features:
    - Handles multiple pages
    - Safely handles empty pages
    - Removes extra whitespace and newlines
    - Returns cleaned, readable text
    """
    
    # Regex patterns for text cleaning
    EXTRA_SPACES = re.compile(r' +')           # Multiple spaces
    EXTRA_NEWLINES = re.compile(r'\n{3,}')    # 3+ consecutive newlines
    MIXED_WHITESPACE = re.compile(r'[ \t]+')  # Tabs and multiple spaces
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Clean and normalize extracted text.
        
        Removes:
        - Extra spaces and tabs
        - Excessive newlines
        - Leading/trailing whitespace per line
        - Special characters that don't add meaning
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # 1. Normalize line endings (convert all to \n)
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # 2. Remove tabs and replace with spaces
        text = text.replace('\t', ' ')
        
        # 3. Remove extra spaces on each line
        text = '\n'.join(
            TextExtractor.EXTRA_SPACES.sub(' ', line).strip()
            for line in text.split('\n')
        )
        
        # 4. Replace 3+ newlines with just 2 (preserve paragraph breaks)
        text = TextExtractor.EXTRA_NEWLINES.sub('\n\n', text)
        
        # 5. Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    @staticmethod
    def extract_page(page, page_num: int = None) -> Tuple[str, bool]:
        """
        Extract text from a single page.
        
        Args:
            page: pdfplumber page object
            page_num: Page number for logging
            
        Returns:
            Tuple of (text, is_empty) where is_empty indicates if page had no text
        """
        try:
            text = page.extract_text()
            
            if not text or not text.strip():
                return "", True  # Empty page
            
            # Clean the extracted text
            cleaned = TextExtractor._clean_text(text)
            
            return cleaned, len(cleaned) == 0
        
        except Exception as e:
            # Log warning but don't fail - some pages might be images
            print(f"Warning: Could not extract text from page {page_num}: {str(e)}")
            return "", True
    
    @staticmethod
    def extract_from_pdf(file_path: Path, verbose: bool = False) -> str:
        """
        Extract text from PDF file.
        
        Handles:
        - Multiple pages
        - Empty pages (skips safely)
        - Text cleaning and normalization
        - Error handling for corrupted/image PDFs
        
        Args:
            file_path: Path to PDF file
            verbose: Print extraction progress
            
        Returns:
            Cleaned, full text from all pages
            
        Raises:
            ValueError: If PDF cannot be read or contains no extractable text
        """
        try:
            text_pages = []
            empty_pages = 0
            
            with pdfplumber.open(file_path) as pdf:
                total_pages = len(pdf.pages)
                
                if verbose:
                    print(f"Extracting text from {total_pages} pages...")
                
                for page_num, page in enumerate(pdf.pages, 1):
                    text, is_empty = TextExtractor.extract_page(page, page_num)
                    
                    if is_empty:
                        empty_pages += 1
                        if verbose:
                            print(f"  Page {page_num}: Empty (skipped)")
                    else:
                        text_pages.append(text)
                        if verbose:
                            print(f"  Page {page_num}: {len(text)} chars")
            
            # Ensure we got some text
            if not text_pages:
                raise ValueError(
                    f"Could not extract text from PDF. "
                    f"{empty_pages}/{total_pages} pages were empty."
                )
            
            # Join pages with clear separation
            full_text = "\n\n".join(text_pages)
            
            if verbose:
                print(f"\nExtraction complete:")
                print(f"  Pages processed: {total_pages}")
                print(f"  Pages with text: {len(text_pages)}")
                print(f"  Empty pages: {empty_pages}")
                print(f"  Total characters: {len(full_text)}")
            
            return full_text
        
        except pdfplumber.PDFException as e:
            raise ValueError(f"Error reading PDF file: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error extracting PDF text: {str(e)}")
    
    @staticmethod
    def extract_pages_separately(file_path: Path) -> List[str]:
        """
        Extract text from PDF with each page as separate item.
        
        Useful for processing pages individually or for analytics.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            List of cleaned text strings, one per page
            
        Raises:
            ValueError: If PDF cannot be read
        """
        try:
            pages_text = []
            
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text, is_empty = TextExtractor.extract_page(page, page_num)
                    if not is_empty:
                        pages_text.append(text)
            
            if not pages_text:
                raise ValueError("Could not extract text from any pages in PDF")
            
            return pages_text
        
        except pdfplumber.PDFException as e:
            raise ValueError(f"Error reading PDF file: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error extracting PDF text: {str(e)}")
    
    @staticmethod
    def extract_with_metadata(file_path: Path) -> dict:
        """
        Extract text and metadata from PDF.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Dictionary with:
            - text: Extracted and cleaned text
            - metadata: PDF metadata
            - page_count: Total pages
            - extracted_pages: Pages with extracted text
            
        Raises:
            ValueError: If PDF cannot be read
        """
        try:
            pages_text = []
            
            with pdfplumber.open(file_path) as pdf:
                metadata = pdf.metadata
                total_pages = len(pdf.pages)
                
                for page_num, page in enumerate(pdf.pages, 1):
                    text, is_empty = TextExtractor.extract_page(page, page_num)
                    if not is_empty:
                        pages_text.append(text)
            
            if not pages_text:
                raise ValueError("Could not extract text from any pages in PDF")
            
            full_text = "\n\n".join(pages_text)
            
            return {
                "text": full_text,
                "metadata": metadata,
                "page_count": total_pages,
                "extracted_pages": len(pages_text),
                "characters": len(full_text)
            }
        
        except pdfplumber.PDFException as e:
            raise ValueError(f"Error reading PDF file: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error extracting PDF text: {str(e)}")
    
    @staticmethod
    def extract_text(file_path: Path) -> str:
        """
        Main extraction method. Extract text from PDF file.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Cleaned, full text from PDF
            
        Raises:
            ValueError: If file is not PDF or extraction fails
        """
        suffix = file_path.suffix.lower()
        
        if suffix != ".pdf":
            raise ValueError(f"Only PDF files are supported. Got: {suffix}")
        
        return TextExtractor.extract_from_pdf(file_path)
