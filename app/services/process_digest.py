from typing import Optional
import logging
from database.repository import Repository
from agent.digest import DigestAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_videos_transcript(limit: Optional[int] = None) -> dict:
    repo = Repository()
    digest = DigestAgent()
    processed = 0
    failed = 0
    errors = []

    articles = repo.get_articles_without_digest(limit=limit)
    logger.info(f"🔍 Tìm được {len(articles)} articles chưa có digest")

    for a in articles:
        try:
            logger.info(f"⏳ Đang xử lý: [{a['type']}] {a['title'][:50]}... (id: {a['id']})")
            
            digest_result = digest.generate_digest(
                title=a["title"],
                content=a["content"],
                article_type=a["type"]
            )

            if digest_result:
                try:
                    repo.create_digest(article_type=a["type"], 
                                article_id=a["id"], 
                                url=a["url"],
                                title=digest_result.title,
                                summary=digest_result.summary)
                    processed += 1
                    logger.info(f"✅ Đã lưu digest cho: {a['id']}")
                except Exception as db_error:
                    logger.error(f"❌ Lỗi lưu DB cho {a['id']}: {str(db_error)}")
                    failed += 1
                    errors.append({"id": a['id'], "error": f"DB Error: {str(db_error)}"})
            else:
                # digest_result is None - có thể do 503 hoặc khác
                logger.warning(f"⚠️  generate_digest trả về None cho: {a['id']}")
                failed += 1
                errors.append({"id": a['id'], "error": "Digest generation returned None (likely 503 error)"})
        
        except Exception as e:
            logger.error(f"❌ Lỗi với bài viết '{a['title']}' (id: {a['id']}): {type(e).__name__}: {str(e)}")
            failed += 1
            errors.append({"id": a['id'], "error": f"{type(e).__name__}: {str(e)}"})
    
    logger.info(f"\n📊 KẾT QUẢ CUỐI CÙNG:")
    logger.info(f"   ✅ Processed: {processed}")
    logger.info(f"   ❌ Failed: {failed}")
    
    if errors:
        logger.info(f"\n📋 DANH SÁCH LỖI:")
        for err in errors:
            logger.info(f"   - {err['id']}: {err['error']}")
    
    return {
        "processed": processed,
        "failed": failed,
        "errors": errors
    }

if __name__ == "__main__":
    result = process_videos_transcript()
    print(result)



