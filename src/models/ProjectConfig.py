from pydantic import BaseModel, Field
from typing import List, Optional

class BusinessRule(BaseModel):
    title: str
    description: str

class Framework(BaseModel):
    name: str
    description: Optional[str] = Field(None, description="Framework description")

class EnvironmentVariable(BaseModel):
    name: str
    description: str

class SecurityConsideration(BaseModel):
    description: Optional[str] = Field(None, description="Description of the security consideration")

class APIEndpoint(BaseModel):
    url: Optional[str] = Field(None, description="API URL")
    description: Optional[str] = Field(None, description="API description")

class ProjectConfig(BaseModel):
    project_name: Optional[str] = Field(None, description="Project name")
    introduction: Optional[str] = Field(None, description="Brief description of the project's objective")
    business_rules: Optional[List[BusinessRule]] = Field(None, description="List of business rules")
    overall_architecture: Optional[str] = Field(None, description="Description of the project's architecture")
    technologies_frameworks: Optional[List[Framework]] = Field(None, description="List of technologies and frameworks used")
    build_instructions: Optional[str] = Field(None, description="Instructions for building the project")
    deployment_instructions: Optional[str] = Field(None, description="Instructions for deploying the project")
    environment_variables: Optional[List[EnvironmentVariable]] = Field(None, description="List of environment variables")
    security_considerations: Optional[List[SecurityConsideration]] = Field(None, description="Security considerations for the project")
    api_documentation: Optional[List[APIEndpoint]] = Field(None, description="Details about the API documentation")
    conclusion: Optional[str] = Field(None, description="Final message and thanks")
    contributing: Optional[str] = Field(None, description="Information on how to contribute to the project")
    license: Optional[str] = Field(None, description="Information about the project's license")
