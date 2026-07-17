import os
from typing import Optional
from pydantic import BaseModel, Field
from design_engine.config import CONFIG

class DesignRequirements(BaseModel):
    business_name: str = Field(..., description="Name of the business")
    platform: str = Field(..., description="Target platform (Instagram, Facebook, etc.)")
    primary_color: str = Field(..., description="Brand primary hex color (e.g. #FF5733)")
    offer: str = Field(..., description="Promotion text or special offer (e.g. 50% OFF)")
    cta: str = Field(..., description="Call to action button text (e.g. SHOP NOW)")
    
    business_type: Optional[str] = Field(None, description="Type of business (e.g. Boutique Coffee)")
    industry: Optional[str] = Field(None, description="Industry sector (e.g. Food & Beverage)")
    target_audience: Optional[str] = Field(None, description="Target demographic details")
    theme: Optional[str] = Field(None, description="Styling theme (Modern, Minimal, Bold)")
    secondary_color: Optional[str] = Field(None, description="Secondary hex color accent")
    product_name: Optional[str] = Field(None, description="Name of the product")
    logo_available: bool = Field(default=False, description="Whether logo placeholder is needed")
    product_image_available: bool = Field(default=False, description="Whether product image placeholder is needed")
    additional_instructions: Optional[str] = Field(None, description="Any specific design instructions")

def get_prompts_dir() -> str:
    prompts_dir = os.path.join(CONFIG.BASE_DIR, "prompts")
    os.makedirs(prompts_dir, exist_ok=True)
    return prompts_dir

class PromptBuilder:
    def __init__(self):
        self.prompts_dir = get_prompts_dir()
        
    def load_prompt_file(self, filename: str) -> str:
        filepath = os.path.join(self.prompts_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read().strip()
        return ""

    def build_system_prompt(self) -> str:
        # Load layout prompt and system prompt directives
        system_content = self.load_prompt_file("system_prompt.txt")
        layout_schema_content = self.load_prompt_file("layout_prompt.txt")
        
        # Build prompt sequence
        return f"{system_content}\n\n[SCHEMA RULES AND LAYOUT EXAMPLES]:\n{layout_schema_content}"

    def build_user_prompt(self, reqs: DesignRequirements) -> str:
        prompt_parts = [
            "Create a Canva-style layout based on these requirements:",
            f"- Business Name: {reqs.business_name}",
            f"- Platform: {reqs.platform}",
            f"- Primary Color: {reqs.primary_color}",
            f"- Offer Copy: {reqs.offer}",
            f"- Call To Action: {reqs.cta}",
        ]
        
        if reqs.business_type:
            prompt_parts.append(f"- Business Category: {reqs.business_type}")
        if reqs.industry:
            prompt_parts.append(f"- Industry: {reqs.industry}")
        if reqs.target_audience:
            prompt_parts.append(f"- Target Audience: {reqs.target_audience}")
        if reqs.theme:
            prompt_parts.append(f"- Visual Theme: {reqs.theme}")
        if reqs.secondary_color:
            prompt_parts.append(f"- Secondary Color Accent: {reqs.secondary_color}")
        if reqs.product_name:
            prompt_parts.append(f"- Product/Service Highlight: {reqs.product_name}")
            
        # Image resources settings
        prompt_parts.append(f"- Logo Placeholder Included: {reqs.logo_available}")
        prompt_parts.append(f"- Product Image Placeholder Included: {reqs.product_image_available}")
        
        if reqs.additional_instructions:
            prompt_parts.append(f"- Additional Instructions: {reqs.additional_instructions}")
            
        return "\n".join(prompt_parts)
