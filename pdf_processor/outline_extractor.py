import fitz
import os
import re
import logging
from .language_support import contains_multilingual, multilingual_numbered_pattern

logger = logging.getLogger('PDFOutlineExtractor')

def is_numbered_form(page_text):
    """Detect numbered forms in multiple languages"""
    lines = [line.strip() for line in page_text.splitlines() if line.strip()]
    if not lines:
        return False
        
    pattern = multilingual_numbered_pattern()
    numbered = [line for line in lines if pattern.match(line)]
    
    # Adjust threshold based on multilingual content
    threshold = 0.4 if contains_multilingual(page_text) else 0.3
    return len(numbered) / len(lines) > threshold

def extract_metadata_title(doc, pdf_path):
    """Extract title from PDF metadata or filename"""
    title = doc.metadata.get("title", "").strip()
    if not title:
        title = os.path.splitext(os.path.basename(pdf_path))[0]
    return title

def process_block(block):
    """Process text block for outline extraction"""
    text = "".join(
        span["text"] for line in block["lines"] for span in line["spans"]
    ).strip()
    
    if not text:
        return None
        
    size = max(span["size"] for line in block["lines"] for span in line["spans"])
    y0 = block["bbox"][1]
    
    return {
        "text": text,
        "size": round(size, 1),
        "page": block.get("page_number", 0) + 1,
        "y0": y0
    }

def extract_blocks(doc):
    """Extract and process all text blocks from document"""
    blocks = []
    for page_num, page in enumerate(doc):
        for block in page.get_text("dict")["blocks"]:
            if block["type"] != 0:  # Skip non-text blocks
                continue
                
            processed = process_block(block)
            if processed:
                blocks.append(processed)
                
    blocks.sort(key=lambda b: (b["page"], b["y0"]))
    return blocks

def determine_heading_levels(blocks):
    """Determine heading levels based on font sizes"""
    unique_sizes = sorted({b["size"] for b in blocks}, reverse=True)
    size_to_level = {size: f"H{min(i+1, 4)}" for i, size in enumerate(unique_sizes[:4])}
    return size_to_level

def build_outline(blocks, size_to_level):
    """Build outline from processed blocks"""
    outline = []
    seen = set()
    
    for block in blocks:
        level = size_to_level.get(block["size"])
        if not level:
            continue
            
        # Apply language-specific rules
        text = block["text"]
        if block["page"] == 1:
            if text.rstrip().endswith((':', '：', '・')):  # Supports EN/JP/CN colons
                level = "H3"
                
        # Deduplication
        key = (level, text, block["page"])
        if key in seen:
            continue
            
        seen.add(key)
        outline.append({
            "level": level,
            "text": text,
            "page": block["page"]
        })
        
    return outline

def get_outline(pdf_path):
    """Main function to extract document outline"""
    try:
        doc = fitz.open(pdf_path)
        logger.info(f"Opened PDF: {os.path.basename(pdf_path)}")
        
        # Process first page for numbered forms
        first_page_text = doc[0].get_text("text")
        if is_numbered_form(first_page_text):
            first_line = next((line.strip() for line in first_page_text.splitlines() if line.strip()), None)
            title = first_line or extract_metadata_title(doc, pdf_path)
            return {"title": title, "outline": []}
        
        # Try built-in TOC first
        toc = doc.get_toc(simple=True)
        if toc:
            return {
                "title": toc[0][1].strip(),
                "outline": [
                    {"level": f"H{lvl}", "text": title.strip(), "page": page}
                    for lvl, title, page in toc
                ]
            }
        
        # Block-based extraction
        raw_title = extract_metadata_title(doc, pdf_path)
        blocks = extract_blocks(doc)
        
        if not blocks:
            return {"title": raw_title, "outline": []}
            
        size_to_level = determine_heading_levels(blocks)
        outline = build_outline(blocks, size_to_level)
        
        # Title extraction
        title_candidates = [
            e["text"] for e in outline
            if e["page"] == 1 and e["level"] in ("H1", "H2")
        ]
        title = " ".join(title_candidates[:3]).strip() if title_candidates else raw_title
        
        logger.info(f"Extracted outline with {len(outline)} headings")
        return {"title": title, "outline": outline}
        
    except Exception as e:
        logger.error(f"Error processing {pdf_path}: {str(e)}")
        return {"title": os.path.basename(pdf_path), "outline": []}