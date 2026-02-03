import { Container } from "@/components/layout/Container";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card } from "@/components/ui/Card";
import { CodeBlock } from "@/components/ui/CodeBlock";
import { PhaseNav } from "@/components/phases/PhaseNav";
import { PhaseNavTop } from "@/components/phases/PhaseNavTop";
import { PhaseTabs } from "@/components/phases/PhaseTabs";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Scaling Production: Enterprise Deployment",
  description: "Deploy multi-agent system to AWS using SageMaker, Bedrock, Aurora",
};

export default function ScalingProductionPage() {
  return (
    <>
      <PageHeader
        title="Scaling Production: Enterprise Deployment"
        subtitle="How the complete system deploys to AWS managed services—preserving your training investment while gaining enterprise scale, security, and operational simplicity"
      >
        <div className="flex flex-wrap gap-4 mt-4">
          <div className="text-base">
            <span className="text-white/60">Direct Investment:</span>
            <span className="ml-2 font-semibold">$163.1K ($11,100 infrastructure)</span>
          </div>
          <div className="text-base">
            <span className="text-white/60">Production Options:</span>
            <span className="ml-2 font-semibold">AWS, Azure, Local</span>
          </div>
          <div className="text-base">
            <span className="text-white/60">Deployment Time:</span>
            <span className="ml-2 font-semibold">~1 week</span>
          </div>
          <div className="text-base">
            <span className="text-white/60">Scale:</span>
            <span className="ml-2 font-semibold">Pilot → Enterprise</span>
          </div>
        </div>
      </PageHeader>

      <PhaseNavTop currentPhase={6} />

      <section className="py-12">
        <Container>
          <PhaseTabs
            vision={
              <>
                <p className="text-xl text-gray-600 mb-6">
                  Transform your $163.1K Direct Investment ($11,100 infrastructure + $152K training programs) into production-ready enterprise AI using AWS managed services—no infrastructure management required
                </p>

                <div className="prose prose-lg max-w-none">
                  <p>
                    The six-phase training process produces production-ready models that deploy directly to AWS managed services. Your embedding model, 14 task SLMs, 3 MoE agents, and orchestrator—all developed through $163.1K Direct Investment ($11,100 infrastructure)—become enterprise-grade AI infrastructure running on SageMaker, Bedrock, and Aurora PostgreSQL. No retraining, no architectural changes, no infrastructure management.
                  </p>

                  <h3 className="text-2xl font-semibold mt-8 mb-4">Strategic Value</h3>
                  <p>
                    Training investment is preserved and amplified through managed services. The file-based Phase 0 registries migrate to Aurora PostgreSQL with automatic backups and multi-AZ deployment. Phase 1 embeddings move from local ChromaDB to Aurora&apos;s pgvector extension—same database, zero additional infrastructure. Phase 2-5 models deploy to SageMaker endpoints with auto-scaling, or integrate with Bedrock for orchestration. Enterprise security, compliance, and operational excellence come built-in. Your team maintains velocity—building AI capabilities—while AWS handles infrastructure operations.
                  </p>

                  <h3 className="text-2xl font-semibold mt-8 mb-4">What&apos;s Delivered</h3>
                  <p>
                    Complete AWS architecture mapping for all six phases. Aurora PostgreSQL hosting both operational data and vector embeddings in a single managed service. SageMaker endpoints serving your custom-trained models with enterprise-grade scaling. Bedrock integration options for orchestration and foundation model augmentation. Production cost models spanning pilot deployment ($800/month) through enterprise scale ($7,500/month). Migration playbook moving from training infrastructure to production in one week.
                  </p>
                </div>
              </>
            }
            approach={
              <>
                <div className="mb-8">
                  <table className="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
                    <thead className="bg-gray-100">
                      <tr>
                        <th className="px-4 py-3 text-left font-semibold text-navy">Component</th>
                        <th className="px-4 py-3 text-left font-semibold text-navy">Local Deployment</th>
                        <th className="px-4 py-3 text-left font-semibold text-navy">AWS Service</th>
                        <th className="px-4 py-3 text-left font-semibold text-navy">Scaling Approach</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      <tr>
                        <td className="px-4 py-3 font-medium">Embedding Model</td>
                        <td className="px-4 py-3 text-gray-600">Sentence-Transformers</td>
                        <td className="px-4 py-3 text-gray-600">SageMaker Endpoint</td>
                        <td className="px-4 py-3 text-gray-600">Auto-scaling inference</td>
                      </tr>
                      <tr className="bg-gray-50">
                        <td className="px-4 py-3 font-medium">Vector Database</td>
                        <td className="px-4 py-3 text-gray-600">ChromaDB</td>
                        <td className="px-4 py-3 text-gray-600">Aurora PostgreSQL + pgvector</td>
                        <td className="px-4 py-3 text-gray-600">Multi-AZ, read replicas</td>
                      </tr>
                      <tr>
                        <td className="px-4 py-3 font-medium">Model Registry</td>
                        <td className="px-4 py-3 text-gray-600">File-based</td>
                        <td className="px-4 py-3 text-gray-600">Aurora PostgreSQL</td>
                        <td className="px-4 py-3 text-gray-600">Managed with auto backups</td>
                      </tr>
                      <tr className="bg-gray-50">
                        <td className="px-4 py-3 font-medium">14 Task SLMs</td>
                        <td className="px-4 py-3 text-gray-600">Llama 3.1 8B + LoRA</td>
                        <td className="px-4 py-3 text-gray-600">SageMaker Multi-Model</td>
                        <td className="px-4 py-3 text-gray-600">Models loaded from S3</td>
                      </tr>
                      <tr>
                        <td className="px-4 py-3 font-medium">3 MoE Agents</td>
                        <td className="px-4 py-3 text-gray-600">mergekit (32B each)</td>
                        <td className="px-4 py-3 text-gray-600">SageMaker Endpoints</td>
                        <td className="px-4 py-3 text-gray-600">Custom containers</td>
                      </tr>
                      <tr className="bg-gray-50">
                        <td className="px-4 py-3 font-medium">Agent Protocol</td>
                        <td className="px-4 py-3 text-gray-600">FastAPI A2A</td>
                        <td className="px-4 py-3 text-gray-600">API Gateway + Lambda/ECS</td>
                        <td className="px-4 py-3 text-gray-600">Serverless or container</td>
                      </tr>
                      <tr>
                        <td className="px-4 py-3 font-medium">Orchestrator</td>
                        <td className="px-4 py-3 text-gray-600">Agno Framework</td>
                        <td className="px-4 py-3 text-gray-600">SageMaker or Bedrock Agents</td>
                        <td className="px-4 py-3 text-gray-600">Managed orchestration</td>
                      </tr>
                    </tbody>
                  </table>
                  <div className="bg-teal/10 px-6 py-4 rounded-lg mt-4">
                    <p className="text-base">
                      <span className="font-semibold text-navy">Estimated AWS Monthly Cost:</span>
                      <span className="text-gray-700 ml-2">~$800 (pilot, 100 users) &rarr; ~$2,400 (mid, 1,000 users) &rarr; ~$7,500 (enterprise, 8,000 users)</span>
                    </p>
                    <p className="text-base text-gray-500 mt-1">Local deployment costs vary by hardware but typically have lower ongoing costs after initial infrastructure investment.</p>
                  </div>
                </div>

                <Card className="bg-gradient-to-br from-navy/5 to-teal/5 border-navy/20 border-t-4 border-t-navy p-12">
                  <p className="text-xl text-gray-600 mb-6">
                    Each phase&apos;s training output maps directly to AWS managed services—preserving your models while gaining enterprise infrastructure
                  </p>

                  <div className="prose prose-lg max-w-none">
                    <h3 className="text-2xl font-semibold mt-4 mb-4">Phase-by-Phase AWS Service Mapping</h3>
                    <p>
                      The six-phase training architecture has a direct AWS equivalent. Phase 0&apos;s file-based registries become Aurora PostgreSQL tables with the same schema—just managed and multi-AZ. Phase 1&apos;s embedding model deploys to a SageMaker endpoint, while embeddings themselves live in Aurora&apos;s pgvector extension alongside operational data. Phase 2&apos;s 14 task SLMs become SageMaker multi-model endpoints, each serving multiple models from S3 with automatic scaling. Phase 3&apos;s MoE agents deploy as SageMaker endpoints with custom routing logic, querying Aurora&apos;s model registry to select experts. Phase 4&apos;s agent-to-agent protocol becomes API Gateway endpoints fronting Lambda or ECS services. Phase 5&apos;s orchestrator runs on SageMaker or integrates with Bedrock&apos;s orchestration capabilities.
                    </p>
                    <p>
                      The architecture doesn&apos;t change—only the infrastructure underneath. Your models run exactly as trained, but AWS handles availability, scaling, security, and operations.
                    </p>

                    <h3 className="text-2xl font-semibold mt-8 mb-4">Aurora as Unified Data Layer</h3>
                    <p>
                      Aurora PostgreSQL with the pgvector extension eliminates infrastructure complexity. A single managed database service handles Phase 0&apos;s operational data (model registry, training data registry, experiment tracking) and Phase 1&apos;s vector embeddings. Instead of managing separate ChromaDB instances, PostgreSQL stores embeddings as vector columns with metadata filtering through standard SQL WHERE clauses. Aurora provides automatic failover, continuous backup to S3, point-in-time recovery, and read replicas for scaling. The database scales from pilot (single instance) to enterprise (multi-AZ cluster with read replicas) without application changes.
                    </p>
                    <p>
                      This unified approach means fewer moving parts, simpler operations, and lower cost at pilot scale. When you query for similar documents in a specific division, it&apos;s a single SQL query combining vector similarity and metadata filters—no cross-system coordination required.
                    </p>

                    <h3 className="text-2xl font-semibold mt-8 mb-4">SageMaker for Model Serving</h3>
                    <p>
                      SageMaker eliminates the complexity of managing GPU instances and model serving infrastructure. Your trained models—embedding model, task SLMs, MoE agents—upload to S3 and deploy to SageMaker endpoints with a few API calls. SageMaker handles model loading, endpoint scaling, health checks, and blue/green deployments. Multi-model endpoints let you serve all 14 Phase 2 task SLMs from a single endpoint, with SageMaker managing model loading and GPU memory. Inference scales from single-instance development endpoints to multi-instance auto-scaling production endpoints without code changes.
                    </p>
                    <p>
                      For Phase 3 MoE agents, SageMaker&apos;s custom inference containers let you implement expert routing logic while SageMaker handles the infrastructure. When query volume increases, add instances. When it decreases, SageMaker scales down automatically. You pay only for what you use.
                    </p>

                    <h3 className="text-2xl font-semibold mt-8 mb-4">Bedrock Integration Options</h3>
                    <p>
                      AWS Bedrock provides two integration paths. First, use Bedrock&apos;s foundation models (Claude, etc.) to augment your custom models—combining your trained task expertise with general reasoning capabilities. Your Phase 2 task SLM extracts structured data from documents, then passes to Bedrock&apos;s Claude for complex analysis requiring broader knowledge. Second, use Bedrock Agents for orchestration instead of training your own Phase 5 orchestrator. Bedrock Agents can route queries to your SageMaker-hosted MoE models while handling conversation state, tool use, and error recovery. This hybrid approach lets you leverage AWS&apos;s managed orchestration while preserving your domain-specific intelligence.
                    </p>
                    <p>
                      The choice is yours: train and deploy your own orchestrator for maximum control, or use Bedrock Agents for faster deployment and managed operations.
                    </p>

                    <h3 className="text-2xl font-semibold mt-8 mb-4">Deployment Flexibility and Optionality</h3>
                    <p>
                      While AWS provides the fastest path to production, the architecture supports multiple deployment targets. Azure offers equivalent services: Azure Database for PostgreSQL with pgvector, Azure Machine Learning for model hosting, Azure OpenAI Service for orchestration. Databricks provides model serving through MLflow with GPU clusters for inference. Local deployment remains possible for regulated industries—models run on your infrastructure with the same API contracts. This optionality preserves your investment regardless of cloud vendor, regulatory requirements, or strategic shifts. The training investment produces portable models, not cloud-locked artifacts.
                    </p>
                  </div>
                </Card>
              </>
            }
            technical={
              <>
                <p className="text-lg text-gray-700 mb-8">
                  Aurora PostgreSQL + pgvector, SageMaker multi-model deployment, ECS agent services, and Bedrock orchestration options
                </p>

                <div className="space-y-16">
                  {/* Part 1: Aurora PostgreSQL + pgvector */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">1. Aurora PostgreSQL + pgvector</h3>
                    <p className="text-gray-700 mb-6">
                      Replace ChromaDB with Aurora PostgreSQL using the pgvector extension for vector similarity search. This consolidates operational data and embeddings in a single managed database.
                    </p>

                    <div className="mb-6">
                      <h4 className="font-semibold mb-3">Database Schema with Vector Column</h4>
                      <CodeBlock
                        language="sql"
                        code={`-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create documents table with vector embeddings
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    metadata JSONB,
    embedding vector(384),  -- all-MiniLM-L6-v2 produces 384-dim vectors
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create HNSW index for fast similarity search
CREATE INDEX ON documents
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Vector similarity query
SELECT id, content, metadata,
       1 - (embedding <=> $1::vector) AS similarity
FROM documents
ORDER BY embedding <=> $1::vector
LIMIT 10;`}
                      />
                    </div>

                    <div className="mb-6">
                      <h4 className="font-semibold mb-3">Terraform Configuration</h4>
                      <CodeBlock
                        language="hcl"
                        code={`resource "aws_rds_cluster" "aurora_postgres" {
  cluster_identifier      = "enterprise-ai-db"
  engine                  = "aurora-postgresql"
  engine_version          = "15.4"
  database_name           = "aidb"
  master_username         = "admin"
  master_password         = var.db_password

  db_cluster_parameter_group_name = aws_rds_cluster_parameter_group.pgvector.name

  backup_retention_period = 7
  preferred_backup_window = "03:00-04:00"

  vpc_security_group_ids = [aws_security_group.aurora.id]
  db_subnet_group_name   = aws_db_subnet_group.aurora.name

  enabled_cloudwatch_logs_exports = ["postgresql"]

  tags = {
    Name = "Enterprise AI Aurora Cluster"
  }
}

resource "aws_rds_cluster_parameter_group" "pgvector" {
  name   = "aurora-postgres-pgvector"
  family = "aurora-postgresql15"

  parameter {
    name  = "shared_preload_libraries"
    value = "pgvector"
  }
}

resource "aws_rds_cluster_instance" "aurora_instance" {
  count              = 2  # Multi-AZ deployment
  identifier         = "enterprise-ai-db-\${count.index}"
  cluster_identifier = aws_rds_cluster.aurora_postgres.id
  instance_class     = "db.r6g.large"
  engine             = aws_rds_cluster.aurora_postgres.engine
  engine_version     = aws_rds_cluster.aurora_postgres.engine_version
}`}
                      />
                    </div>
                  </div>

                  {/* Part 2: SageMaker Multi-Model Deployment */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">2. SageMaker Multi-Model Deployment</h3>
                    <p className="text-gray-700 mb-6">
                      Deploy the embedding model and three MoE agents to SageMaker for managed inference with auto-scaling.
                    </p>

                    <div className="mb-6">
                      <h4 className="font-semibold mb-3">Model Deployment Script</h4>
                      <CodeBlock
                        language="python"
                        code={`import boto3
import sagemaker
from sagemaker.huggingface import HuggingFaceModel

session = sagemaker.Session()
role = "arn:aws:iam::ACCOUNT:role/SageMakerExecutionRole"

# Deploy embedding model
embedding_model = HuggingFaceModel(
    model_data="s3://your-bucket/models/embedding-model.tar.gz",
    role=role,
    transformers_version="4.37",
    pytorch_version="2.1",
    py_version="py310",
)

embedding_endpoint = embedding_model.deploy(
    initial_instance_count=1,
    instance_type="ml.g5.xlarge",
    endpoint_name="embedding-model",
    container_startup_health_check_timeout=600,
)

# Deploy MoE agents (fundraising, business-dev, field-ops)
moe_agents = [
    ("fundraising-moe", "s3://your-bucket/models/fundraising-moe.tar.gz"),
    ("business-dev-moe", "s3://your-bucket/models/business-dev-moe.tar.gz"),
    ("field-ops-moe", "s3://your-bucket/models/field-ops-moe.tar.gz"),
]

for name, model_data in moe_agents:
    moe_model = HuggingFaceModel(
        model_data=model_data,
        role=role,
        transformers_version="4.37",
        pytorch_version="2.1",
        py_version="py310",
        env={
            "SAGEMAKER_MODEL_SERVER_TIMEOUT": "600",
            "SAGEMAKER_MODEL_SERVER_WORKERS": "1",
        }
    )

    endpoint = moe_model.deploy(
        initial_instance_count=1,
        instance_type="ml.g5.2xlarge",  # Larger for MoE models
        endpoint_name=name,
    )
    print(f"Deployed {name}: {endpoint.endpoint_name}")`}
                      />
                    </div>

                    <div className="mb-6">
                      <h4 className="font-semibold mb-3">Auto-Scaling Configuration</h4>
                      <CodeBlock
                        language="python"
                        code={`import boto3

client = boto3.client('application-autoscaling')

# Register SageMaker endpoint as scalable target
client.register_scalable_target(
    ServiceNamespace='sagemaker',
    ResourceId=f'endpoint/fundraising-moe/variant/AllTraffic',
    ScalableDimension='sagemaker:variant:DesiredInstanceCount',
    MinCapacity=1,
    MaxCapacity=4,
)

# Target tracking policy based on invocations per instance
client.put_scaling_policy(
    PolicyName='moe-scale-on-invocations',
    ServiceNamespace='sagemaker',
    ResourceId=f'endpoint/fundraising-moe/variant/AllTraffic',
    ScalableDimension='sagemaker:variant:DesiredInstanceCount',
    PolicyType='TargetTrackingScaling',
    TargetTrackingScalingPolicyConfiguration={
        'TargetValue': 1000.0,  # Target 1000 invocations per minute per instance
        'PredefinedMetricSpecification': {
            'PredefinedMetricType': 'SageMakerVariantInvocationsPerInstance',
        },
        'ScaleInCooldown': 300,
        'ScaleOutCooldown': 60,
    },
)`}
                      />
                    </div>
                  </div>

                  {/* Part 3: MoE Inference Handler */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">3. MoE Inference Handler</h3>
                    <p className="text-gray-700 mb-6">
                      Custom inference script for MoE models deployed to SageMaker.
                    </p>

                    <div className="mb-6">
                      <h4 className="font-semibold mb-3">Inference Handler (inference.py)</h4>
                      <CodeBlock
                        language="python"
                        code={`import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def model_fn(model_dir):
    """Load MoE model from SageMaker model directory"""
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForCausalLM.from_pretrained(
        model_dir,
        torch_dtype=torch.float16,
        device_map="auto",
    )
    return {"model": model, "tokenizer": tokenizer}

def predict_fn(data, model_and_tokenizer):
    """Run inference on MoE model"""
    model = model_and_tokenizer["model"]
    tokenizer = model_and_tokenizer["tokenizer"]

    prompt = data.pop("inputs", "")
    parameters = data.pop("parameters", {})

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=parameters.get("max_new_tokens", 512),
            temperature=parameters.get("temperature", 0.7),
            top_p=parameters.get("top_p", 0.9),
            do_sample=parameters.get("do_sample", True),
        )

    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return {"generated_text": generated_text}`}
                      />
                    </div>

                    <div className="mb-6">
                      <h4 className="font-semibold mb-3">Model Package Structure</h4>
                      <CodeBlock
                        language="python"
                        code={`# Directory structure for SageMaker model artifact
model.tar.gz/
├── code/
│   ├── inference.py          # Custom inference handler
│   └── requirements.txt      # Dependencies
├── model/
│   ├── config.json
│   ├── pytorch_model.bin     # MoE model weights
│   ├── tokenizer.json
│   └── tokenizer_config.json

# Package model
import tarfile
import os

def package_model(model_dir, output_path):
    with tarfile.open(output_path, "w:gz") as tar:
        tar.add(model_dir, arcname=".")
    print(f"Model packaged to {output_path}")

package_model("./fundraising-moe", "fundraising-moe.tar.gz")
# Upload to S3: aws s3 cp fundraising-moe.tar.gz s3://your-bucket/models/`}
                      />
                    </div>
                  </div>

                  {/* Part 4: Agent Services on ECS */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">4. Agent Services on ECS</h3>
                    <p className="text-gray-700 mb-6">
                      Deploy FastAPI agent services to ECS Fargate with Application Load Balancer.
                    </p>

                    <div className="mb-6">
                      <h4 className="font-semibold mb-3">FastAPI Agent Service</h4>
                      <CodeBlock
                        language="python"
                        code={`from fastapi import FastAPI
import boto3
import json

app = FastAPI()
sagemaker_runtime = boto3.client('sagemaker-runtime')

ENDPOINT_NAME = "fundraising-moe"

@app.post("/agent/invoke")
async def invoke_agent(request: dict):
    """Invoke MoE agent via SageMaker endpoint"""
    prompt = request.get("prompt", "")

    response = sagemaker_runtime.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        ContentType='application/json',
        Body=json.dumps({
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 512,
                "temperature": 0.7,
            }
        })
    )

    result = json.loads(response['Body'].read().decode())
    return {"response": result["generated_text"]}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Run with: uvicorn main:app --host 0.0.0.0 --port 8000`}
                      />
                    </div>

                    <div className="mb-6">
                      <h4 className="font-semibold mb-3">ECS Deployment with Terraform</h4>
                      <CodeBlock
                        language="hcl"
                        code={`resource "aws_ecs_cluster" "agents" {
  name = "enterprise-ai-agents"
}

resource "aws_ecs_task_definition" "fundraising_agent" {
  family                   = "fundraising-agent"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "1024"
  memory                   = "2048"
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([{
    name  = "fundraising-agent"
    image = "\${aws_ecr_repository.agents.repository_url}:fundraising"

    portMappings = [{
      containerPort = 8000
      protocol      = "tcp"
    }]

    environment = [
      { name = "SAGEMAKER_ENDPOINT", value = "fundraising-moe" },
      { name = "AWS_REGION", value = var.aws_region },
    ]

    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = "/ecs/fundraising-agent"
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "ecs"
      }
    }
  }])
}

resource "aws_ecs_service" "fundraising_agent" {
  name            = "fundraising-agent"
  cluster         = aws_ecs_cluster.agents.id
  task_definition = aws_ecs_task_definition.fundraising_agent.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.private[*].id
    security_groups  = [aws_security_group.agent_service.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.fundraising.arn
    container_name   = "fundraising-agent"
    container_port   = 8000
  }
}

resource "aws_lb" "agents" {
  name               = "agent-services-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id
}

resource "aws_apigatewayv2_api" "agents" {
  name          = "enterprise-ai-agents"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "fundraising" {
  api_id             = aws_apigatewayv2_api.agents.id
  integration_type   = "HTTP_PROXY"
  integration_uri    = aws_lb.agents.arn
  integration_method = "ANY"
}`}
                      />
                    </div>
                  </div>

                  {/* Part 5: Orchestrator Options */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">5. Orchestrator Options</h3>
                    <p className="text-gray-700 mb-6">
                      Choose between deploying your custom-trained orchestrator or using Amazon Bedrock Agents.
                    </p>

                    <div className="mb-6">
                      <h4 className="font-semibold mb-3">Option A: Custom Orchestrator on ECS</h4>
                      <CodeBlock
                        language="python"
                        code={`from agno import Agno
from agno.models.amazon_bedrock import BedrockChat
import boto3

# Initialize Agno with custom orchestrator model
orchestrator = Agno(
    model=BedrockChat(
        model="your-custom-orchestrator",  # Deployed to Bedrock
        region="us-east-1",
    ),
    agents=[
        "http://fundraising-agent:8000",
        "http://business-dev-agent:8000",
        "http://field-ops-agent:8000",
    ],
)

@app.post("/orchestrate")
async def orchestrate_request(request: dict):
    """Route request through trained orchestrator"""
    user_query = request.get("query", "")

    result = await orchestrator.run(
        query=user_query,
        context=request.get("context", {}),
    )

    return {
        "response": result.response,
        "agents_used": result.agents_used,
        "confidence": result.confidence,
    }`}
                      />
                    </div>

                    <div className="mb-6">
                      <h4 className="font-semibold mb-3">Option B: Amazon Bedrock Agents</h4>
                      <CodeBlock
                        language="python"
                        code={`import boto3

bedrock_agent = boto3.client('bedrock-agent')

# Create Bedrock Agent with action groups for each division
response = bedrock_agent.create_agent(
    agentName='enterprise-orchestrator',
    agentResourceRoleArn='arn:aws:iam::ACCOUNT:role/BedrockAgentRole',
    foundationModel='anthropic.claude-3-sonnet-20240229-v1:0',
    instruction='''You are an enterprise AI orchestrator coordinating three division agents:
    - Fundraising: investor intelligence, portfolio tracking
    - Business Development: RFP tracking, competitive intelligence
    - Field Operations: project performance, local market data

    Route requests to appropriate agents based on intent.''',
)

# Define action groups for each agent
for agent_name in ['fundraising', 'business-dev', 'field-ops']:
    bedrock_agent.create_agent_action_group(
        agentId=response['agent']['agentId'],
        agentVersion='DRAFT',
        actionGroupName=f'{agent_name}-actions',
        actionGroupExecutor={
            'lambda': f'arn:aws:lambda:REGION:ACCOUNT:function:{agent_name}-agent'
        },
        apiSchema={
            'payload': json.dumps({
                "openapi": "3.0.0",
                "info": {"title": f"{agent_name} Agent API"},
                "paths": {
                    "/invoke": {
                        "post": {
                            "description": f"Invoke {agent_name} agent",
                            "parameters": [],
                            "requestBody": {"required": True},
                        }
                    }
                }
            })
        },
    )`}
                      />
                    </div>
                  </div>

                  {/* Part 6: Monitoring & Backup */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">6. Monitoring & Backup</h3>
                    <p className="text-gray-700 mb-6">
                      Comprehensive monitoring with CloudWatch and automated backup strategies.
                    </p>

                    <div className="mb-6">
                      <h4 className="font-semibold mb-3">CloudWatch Monitoring</h4>
                      <CodeBlock
                        language="python"
                        code={`import boto3
from datetime import datetime, timedelta

cloudwatch = boto3.client('cloudwatch')

def create_dashboard():
    """Create CloudWatch dashboard for enterprise AI system"""
    dashboard_body = {
        "widgets": [
            {
                "type": "metric",
                "properties": {
                    "metrics": [
                        ["AWS/SageMaker", "ModelLatency",
                         {"stat": "Average", "label": "Avg Latency"}],
                        [".", ".", {"stat": "p99", "label": "P99 Latency"}],
                    ],
                    "period": 300,
                    "stat": "Average",
                    "region": "us-east-1",
                    "title": "SageMaker Endpoint Latency"
                }
            },
            {
                "type": "metric",
                "properties": {
                    "metrics": [
                        ["AWS/RDS", "DatabaseConnections",
                         {"stat": "Average"}],
                        [".", "CPUUtilization", {"stat": "Average"}],
                        [".", "FreeableMemory", {"stat": "Average"}],
                    ],
                    "period": 300,
                    "stat": "Average",
                    "region": "us-east-1",
                    "title": "Aurora Performance"
                }
            },
            {
                "type": "log",
                "properties": {
                    "query": """fields @timestamp, @message
                        | filter @message like /ERROR/
                        | sort @timestamp desc
                        | limit 20""",
                    "region": "us-east-1",
                    "title": "Recent Errors",
                    "logGroupNames": [
                        "/aws/sagemaker/Endpoints/fundraising-moe",
                        "/ecs/fundraising-agent",
                    ]
                }
            },
        ]
    }

    cloudwatch.put_dashboard(
        DashboardName='EnterpriseAI-Production',
        DashboardBody=json.dumps(dashboard_body)
    )

# Set up alarms
cloudwatch.put_metric_alarm(
    AlarmName='HighSageMakerLatency',
    ComparisonOperator='GreaterThanThreshold',
    EvaluationPeriods=2,
    MetricName='ModelLatency',
    Namespace='AWS/SageMaker',
    Period=300,
    Statistic='Average',
    Threshold=5000.0,  # 5 seconds
    ActionsEnabled=True,
    AlarmActions=['arn:aws:sns:REGION:ACCOUNT:alerts'],
    AlarmDescription='Alert when model latency exceeds 5s',
)`}
                      />
                    </div>

                    <div className="mb-6">
                      <h4 className="font-semibold mb-3">Backup Strategy</h4>
                      <CodeBlock
                        language="hcl"
                        code={`# Aurora automated backups
resource "aws_rds_cluster" "aurora_postgres" {
  backup_retention_period      = 30  # 30 days
  preferred_backup_window      = "03:00-04:00"
  copy_tags_to_snapshot        = true
  deletion_protection          = true

  # Enable continuous backup to S3
  enable_http_endpoint = true

  tags = {
    BackupSchedule = "daily"
  }
}

# S3 bucket for model artifacts and backups
resource "aws_s3_bucket" "model_artifacts" {
  bucket = "enterprise-ai-models-\${var.account_id}"

  versioning {
    enabled = true
  }

  lifecycle_rule {
    enabled = true

    noncurrent_version_expiration {
      days = 90
    }
  }
}

# AWS Backup plan for comprehensive protection
resource "aws_backup_plan" "enterprise_ai" {
  name = "enterprise-ai-backup"

  rule {
    rule_name         = "daily_backup"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 3 * * ? *)"  # 3 AM daily

    lifecycle {
      delete_after = 30
    }
  }

  rule {
    rule_name         = "weekly_backup"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 3 ? * 1 *)"  # 3 AM every Monday

    lifecycle {
      delete_after = 90
    }
  }
}

resource "aws_backup_selection" "aurora" {
  plan_id = aws_backup_plan.enterprise_ai.id
  name    = "aurora-backup-selection"

  resources = [
    aws_rds_cluster.aurora_postgres.arn
  ]
}`}
                      />
                    </div>
                  </div>

                  {/* Part 7: Cost Analysis */}
                  <div>
                    <h3 className="text-2xl font-semibold mb-4">7. Cost Analysis</h3>
                    <p className="text-gray-700 mb-6">
                      Monthly cost estimates for different deployment scales.
                    </p>

                    <div className="mb-6">
                      <h4 className="font-semibold mb-3">Pilot Scale (10-50 users)</h4>
                      <CodeBlock
                        language="text"
                        code={`Infrastructure:
- SageMaker Endpoints:
  * 1x ml.g5.xlarge (embedding): $1.41/hr × 730hr = $1,029/mo
  * 1x ml.g5.2xlarge (MoE): $2.03/hr × 730hr = $1,482/mo
- Aurora PostgreSQL:
  * 1x db.r6g.large: $0.29/hr × 730hr = $212/mo
  * Storage (100GB): $0.10/GB = $10/mo
- ECS Fargate:
  * 3 agent services (1vCPU, 2GB each): ~$50/mo
- Data Transfer: ~$20/mo
- CloudWatch Logs: ~$10/mo

Total: ~$2,813/mo (~$800/mo with Reserved Instances and Savings Plans)`}
                      />
                    </div>

                    <div className="mb-6">
                      <h4 className="font-semibold mb-3">Growth Scale (50-200 users)</h4>
                      <CodeBlock
                        language="text"
                        code={`Infrastructure:
- SageMaker Endpoints:
  * 1x ml.g5.xlarge (embedding): $1,029/mo
  * 3x ml.g5.2xlarge (3 MoE agents): $4,446/mo
- Aurora PostgreSQL:
  * 2x db.r6g.xlarge (writer + reader): $0.58/hr × 730hr × 2 = $846/mo
  * Storage (500GB): $50/mo
- ECS Fargate:
  * 3 agent services (2vCPU, 4GB each): ~$150/mo
- Application Load Balancer: ~$25/mo
- Data Transfer: ~$100/mo
- CloudWatch: ~$50/mo

Total: ~$6,696/mo (~$2,400/mo with 3-year Reserved Instances)`}
                      />
                    </div>

                    <div className="mb-6">
                      <h4 className="font-semibold mb-3">Enterprise Scale (200-1000 users)</h4>
                      <CodeBlock
                        language="text"
                        code={`Infrastructure:
- SageMaker Endpoints:
  * 2x ml.g5.2xlarge (embedding): $2,964/mo
  * 6x ml.g5.4xlarge (3 MoE agents, 2 instances each): $17,568/mo
- Aurora PostgreSQL:
  * 1x db.r6g.2xlarge (writer): $0.87/hr × 730hr = $635/mo
  * 2x db.r6g.xlarge (readers): $846/mo
  * Storage (2TB): $200/mo
- ECS Fargate:
  * 3 agent services (4vCPU, 8GB each, 3 replicas): ~$450/mo
- Application Load Balancer: ~$50/mo
- NAT Gateway: ~$45/mo
- Data Transfer: ~$500/mo
- CloudWatch + X-Ray: ~$200/mo

Total: ~$23,458/mo (~$7,500/mo with Reserved Instances and auto-scaling optimization)`}
                      />
                    </div>

                    <div className="mt-8">
                      <h4 className="font-semibold mb-3">Cost Comparison: AWS Managed vs Self-Managed</h4>
                      <div className="overflow-x-auto">
                        <table className="min-w-full border border-gray-300">
                          <thead className="bg-gray-50">
                            <tr>
                              <th className="border border-gray-300 px-4 py-2 text-left">Component</th>
                              <th className="border border-gray-300 px-4 py-2 text-left">AWS Managed</th>
                              <th className="border border-gray-300 px-4 py-2 text-left">Self-Managed (EC2)</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td className="border border-gray-300 px-4 py-2">Model Hosting</td>
                              <td className="border border-gray-300 px-4 py-2">SageMaker (higher cost, zero ops)</td>
                              <td className="border border-gray-300 px-4 py-2">EC2 G5 instances (~30% cheaper)</td>
                            </tr>
                            <tr className="bg-gray-50">
                              <td className="border border-gray-300 px-4 py-2">Database</td>
                              <td className="border border-gray-300 px-4 py-2">Aurora (managed backups, HA)</td>
                              <td className="border border-gray-300 px-4 py-2">PostgreSQL on EC2 (~40% cheaper)</td>
                            </tr>
                            <tr>
                              <td className="border border-gray-300 px-4 py-2">Operational Overhead</td>
                              <td className="border border-gray-300 px-4 py-2">Minimal (managed services)</td>
                              <td className="border border-gray-300 px-4 py-2">Significant (requires DevOps team)</td>
                            </tr>
                            <tr className="bg-gray-50">
                              <td className="border border-gray-300 px-4 py-2">Auto-scaling</td>
                              <td className="border border-gray-300 px-4 py-2">Built-in (SageMaker + Aurora)</td>
                              <td className="border border-gray-300 px-4 py-2">Custom implementation required</td>
                            </tr>
                            <tr>
                              <td className="border border-gray-300 px-4 py-2">Backup/Recovery</td>
                              <td className="border border-gray-300 px-4 py-2">Automated (AWS Backup)</td>
                              <td className="border border-gray-300 px-4 py-2">Manual setup and monitoring</td>
                            </tr>
                            <tr className="bg-gray-50">
                              <td className="border border-gray-300 px-4 py-2 font-semibold">Best For</td>
                              <td className="border border-gray-300 px-4 py-2">Small teams, fast iteration</td>
                              <td className="border border-gray-300 px-4 py-2">Large teams, cost optimization</td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Next Steps CTA */}
                <div className="bg-gradient-to-br from-navy to-teal text-white p-12 rounded-lg text-center mt-16">
                  <h2 className="text-3xl font-bold mb-4">
                    Ready to Deploy Your Multi-Agent System
                  </h2>
                  <p className="text-xl text-white/90 mb-8 max-w-3xl mx-auto">
                    You&apos;ve completed the training pipeline across all five phases. Now deploy to production using AWS managed services for enterprise-scale reliability.
                  </p>
                  <div className="flex flex-col sm:flex-row gap-4 justify-center">
                    <a
                      href="/solution"
                      className="inline-block px-8 py-4 bg-white text-navy font-medium rounded-md hover:bg-white/90 transition-colors"
                    >
                      Review All Phases
                    </a>
                    <a
                      href="https://github.com/emergent-enterprise-ai"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-block px-8 py-4 bg-teal text-white font-medium rounded-md hover:bg-teal/90 transition-colors"
                    >
                      View on GitHub
                    </a>
                  </div>
                </div>
              </>
            }
          />
        </Container>
      </section>

      <PhaseNav currentPhase={6} />
    </>
  );
}
