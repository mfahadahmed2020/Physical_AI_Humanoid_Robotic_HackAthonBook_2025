from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.assessment import Assessment as AssessmentModel, AssessmentSubmission as AssessmentSubmissionModel
from ..models.assessment_pydantic import AssessmentCreate, AssessmentUpdate, AssessmentSubmissionCreate, AssessmentSubmissionUpdate


class AssessmentService:
    @staticmethod
    def get_assessment_by_id(db: Session, assessment_id: int) -> Optional[AssessmentModel]:
        return db.query(AssessmentModel).filter(AssessmentModel.id == assessment_id).first()

    @staticmethod
    def get_assessments_by_chapter(db: Session, chapter_id: int) -> List[AssessmentModel]:
        return db.query(AssessmentModel).filter(AssessmentModel.chapter_id == chapter_id).all()

    @staticmethod
    def get_assessments(db: Session, skip: int = 0, limit: int = 100) -> List[AssessmentModel]:
        return db.query(AssessmentModel).offset(skip).limit(limit).all()

    @staticmethod
    def create_assessment(db: Session, assessment: AssessmentCreate) -> AssessmentModel:
        db_assessment = AssessmentModel(
            chapter_id=assessment.chapter_id,
            title=assessment.title,
            description=assessment.description,
            assessment_type=assessment.assessment_type,
            questions=assessment.questions,
            max_score=assessment.max_score,
            time_limit=assessment.time_limit
        )

        db.add(db_assessment)
        db.commit()
        db.refresh(db_assessment)

        return db_assessment

    @staticmethod
    def update_assessment(db: Session, assessment_id: int, assessment_update: AssessmentUpdate) -> Optional[AssessmentModel]:
        db_assessment = db.query(AssessmentModel).filter(AssessmentModel.id == assessment_id).first()

        if not db_assessment:
            return None

        # Update fields if provided
        if assessment_update.title is not None:
            db_assessment.title = assessment_update.title
        if assessment_update.description is not None:
            db_assessment.description = assessment_update.description
        if assessment_update.assessment_type is not None:
            db_assessment.assessment_type = assessment_update.assessment_type
        if assessment_update.questions is not None:
            db_assessment.questions = assessment_update.questions
        if assessment_update.max_score is not None:
            db_assessment.max_score = assessment_update.max_score
        if assessment_update.time_limit is not None:
            db_assessment.time_limit = assessment_update.time_limit

        db.commit()
        db.refresh(db_assessment)

        return db_assessment

    @staticmethod
    def delete_assessment(db: Session, assessment_id: int) -> bool:
        db_assessment = db.query(AssessmentModel).filter(AssessmentModel.id == assessment_id).first()

        if not db_assessment:
            return False

        db.delete(db_assessment)
        db.commit()

        return True

    @staticmethod
    def get_assessment_submission_by_id(db: Session, submission_id: int) -> Optional[AssessmentSubmissionModel]:
        return db.query(AssessmentSubmissionModel).filter(AssessmentSubmissionModel.id == submission_id).first()

    @staticmethod
    def get_assessment_submissions_by_assessment(db: Session, assessment_id: int) -> List[AssessmentSubmissionModel]:
        return db.query(AssessmentSubmissionModel).filter(AssessmentSubmissionModel.assessment_id == assessment_id).all()

    @staticmethod
    def get_assessment_submissions_by_user(db: Session, user_id: int) -> List[AssessmentSubmissionModel]:
        return db.query(AssessmentSubmissionModel).filter(AssessmentSubmissionModel.user_id == user_id).all()

    @staticmethod
    def get_assessment_submission(db: Session, assessment_id: int, user_id: int) -> Optional[AssessmentSubmissionModel]:
        return db.query(AssessmentSubmissionModel).filter(
            AssessmentSubmissionModel.assessment_id == assessment_id,
            AssessmentSubmissionModel.user_id == user_id
        ).first()

    @staticmethod
    def create_assessment_submission(db: Session, submission: AssessmentSubmissionCreate) -> AssessmentSubmissionModel:
        # Check if submission already exists for this user and assessment
        existing_submission = db.query(AssessmentSubmissionModel).filter(
            AssessmentSubmissionModel.assessment_id == submission.assessment_id,
            AssessmentSubmissionModel.user_id == submission.user_id
        ).first()

        if existing_submission:
            # Update existing submission instead of creating a new one
            return AssessmentService.update_assessment_submission(
                db,
                existing_submission.id,
                AssessmentSubmissionUpdate(answers=submission.answers)
            )

        db_submission = AssessmentSubmissionModel(
            assessment_id=submission.assessment_id,
            user_id=submission.user_id,
            answers=submission.answers
        )

        db.add(db_submission)
        db.commit()
        db.refresh(db_submission)

        return db_submission

    @staticmethod
    def update_assessment_submission(db: Session, submission_id: int, submission_update: AssessmentSubmissionUpdate) -> Optional[AssessmentSubmissionModel]:
        db_submission = db.query(AssessmentSubmissionModel).filter(AssessmentSubmissionModel.id == submission_id).first()

        if not db_submission:
            return None

        # Update fields if provided
        if submission_update.answers is not None:
            db_submission.answers = submission_update.answers

        db.commit()
        db.refresh(db_submission)

        return db_submission

    @staticmethod
    def grade_assessment_submission(db: Session, submission_id: int, score: int, feedback: Optional[str] = None) -> Optional[AssessmentSubmissionModel]:
        db_submission = db.query(AssessmentSubmissionModel).filter(AssessmentSubmissionModel.id == submission_id).first()

        if not db_submission:
            return None

        # Update score and feedback
        db_submission.score = score
        db_submission.feedback = feedback
        db_submission.status = "GRADED"

        db.commit()
        db.refresh(db_submission)

        return db_submission