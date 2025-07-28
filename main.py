import os
import json
import logging
from pdf_processor.outline_extractor import get_outline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('PDFOutlineExtractor')

def main():
    inp_dir = "/app/input"
    out_dir = "/app/output"
    os.makedirs(out_dir, exist_ok=True)
    logger.info(f"Starting PDF processing. Input: {inp_dir}, Output: {out_dir}")

    processed = 0
    for fname in os.listdir(inp_dir):
        if not fname.lower().endswith(".pdf"):
            continue
            
        pdf_path = os.path.join(inp_dir, fname)
        try:
            logger.info(f"Processing: {fname}")
            result = get_outline(pdf_path)
            
            json_name = os.path.splitext(fname)[0] + ".json"
            output_path = os.path.join(out_dir, json_name)
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            processed += 1
            logger.info(f"Generated: {json_name}")
            
        except Exception as e:
            logger.error(f"Failed to process {fname}: {str(e)}")

    logger.info(f"Completed. Processed {processed} files. Output in {out_dir}")

if __name__ == "__main__":
    main()