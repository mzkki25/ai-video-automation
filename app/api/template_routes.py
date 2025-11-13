from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.Database import get_db
from app.models.User import User
from app.models.Template import Template
from app.schemas.TemplateSchemas import TemplateCreate, TemplateResponse, TemplateListResponse
from app.middleware.AuthMiddleware import get_current_user

router = APIRouter(prefix="/api/templates", tags=["templates"])

@router.get("")
def get_templates(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    templates = db.query(Template).filter(Template.user_id == current_user.id).all()
    return [{
        "id": str(t.id),
        "name": t.name,
        "description": getattr(t, 'description', ''),
        "data": {
            "nama_produk": t.nama_produk,
            "target_audiens": t.target_audiens,
            "usp": t.usp,
            "cta": t.cta
        }
    } for t in templates]

@router.post("")
def create_template(
    request: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    data = request.get('data', {})
    template = Template(
        user_id=current_user.id,
        name=request.get('name'),
        nama_produk=data.get('nama_produk'),
        target_audiens=data.get('target_audiens'),
        usp=data.get('usp'),
        cta=data.get('cta')
    )
    db.add(template)
    db.commit()
    db.refresh(template)
    return {"id": str(template.id), "name": template.name}

@router.get("/{template_id}")
def get_template(
    template_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    template = db.query(Template).filter(
        Template.id == template_id,
        Template.user_id == current_user.id
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return {
        "id": str(template.id),
        "name": template.name,
        "data": {
            "nama_produk": template.nama_produk,
            "target_audiens": template.target_audiens,
            "usp": template.usp,
            "cta": template.cta
        }
    }

@router.delete("/{template_id}")
def delete_template(
    template_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    template = db.query(Template).filter(
        Template.id == template_id,
        Template.user_id == current_user.id
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    db.delete(template)
    db.commit()
    
    return {"message": "Template deleted successfully"}
