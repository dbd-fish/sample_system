from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from uuid import UUID
from app.models.report import Report
from app.repositories.report_repository import ReportRepository
from app.schemas.report import RequestReport, ResponseReport
from app.config.test_data import TestData
import structlog
from sqlalchemy.exc import SQLAlchemyError


logger = structlog.get_logger()


async def create_report(report_data: RequestReport, db: AsyncSession) -> ResponseReport:
    """
    新しいレポートを作成するサービス関数。
    """
    logger.info("create_report - start", report_data=report_data)

    new_report = Report(
        user_id=TestData.TEST_USER_ID_1,
        title=report_data.title,
        content=report_data.content,
        format=report_data.format,
        visibility=report_data.visibility,
    )

    try:
        saved_report = await ReportRepository.create_report(db, new_report)
        logger.info("create_report - success", report_id=saved_report.report_id)
        return ResponseReport.model_validate(saved_report)
    except SQLAlchemyError as e:
        logger.error("create_report - error", error=str(e))
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        logger.info("create_report - end")


async def update_report(report_id: str, updated_data: RequestReport, db: AsyncSession) -> ResponseReport:
    """
    レポートを更新するサービス関数。
    """
    logger.info("update_report - start", report_id=report_id, updated_data=updated_data)

    report = await ReportRepository.get_report_by_id(db, UUID(report_id))
    if not report:
        logger.warning("update_report - report not found", report_id=report_id)
        raise HTTPException(status_code=404, detail="Report not found")

    for key, value in updated_data.model_dump(exclude_unset=True).items():
        setattr(report, key, value)

    try:
        updated_report = await ReportRepository.update_report(db, report)
        logger.info("update_report - success", report_id=updated_report.report_id)
        return ResponseReport.model_validate(updated_report)
    except SQLAlchemyError as e:
        logger.error("update_report - error", error=str(e))
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        logger.info("update_report - end")


async def delete_report(report_id: str, db: AsyncSession) -> dict:
    """
    レポートを論理削除するサービス関数。
    """
    logger.info("delete_report - start", report_id=report_id)

    report = await ReportRepository.fetch_report_for_update(db, UUID(report_id))
    if not report:
        logger.warning("delete_report - report not found", report_id=report_id)
        raise HTTPException(status_code=404, detail="Report not found")

    try:
        await ReportRepository.delete_report(db, report)
        logger.info("delete_report - success", report_id=report.report_id)
        return {"message": "Report deleted successfully"}
    except SQLAlchemyError as e:
        logger.error("delete_report - error", error=str(e))
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        logger.info("delete_report - end")


async def get_report_by_id_service(report_id: str, db: AsyncSession) -> ResponseReport:
    """
    指定されたIDのレポートを取得するサービス関数。
    """
    logger.info("get_report_by_id_service - start", report_id=report_id)

    report = await ReportRepository.get_report_by_id(db, UUID(report_id))
    if not report:
        logger.warning("get_report_by_id_service - not found", report_id=report_id)
        raise HTTPException(status_code=404, detail="Report not found")

    logger.info("get_report_by_id_service - success", report_id=report.report_id)
    return ResponseReport.model_validate(report)
