# AGENT-CORE-AWS – Intelligent Agents with Amazon Bedrock

🚀 **AGENT-CORE-AWS** is a hands-on crash course for building and deploying intelligent agents using **Amazon Bedrock AgentCore**. This repository contains progressive examples demonstrating how to create AI agents that leverage language models, RAG (Retrieval-Augmented Generation), and sophisticated memory management.


## 🎯 What You Will Learn

In this hands-on project, you will learn how to:

* 🛠️ Build intelligent agents using **Amazon Bedrock AgentCore**
* 📚 Implement **RAG pipelines** for context-aware AI responses
* 🔌 Create **custom tools** to extend agent capabilities
* 🧠 Manage **agent memory and sessions** for conversational continuity
* 🚀 Deploy and invoke agents in **production environments**
* ⚡ Integrate high-performance inference using **Groq LLMs**
* 🤗 Use **Hugging Face models** for embeddings and NLP tasks


---

## 📂 Project Structure

```
Bedrock-AgentCore-AWS-RAG-Hands-On/
│
├── .bedrock_agentcore/      # Bedrock AgentCore configuration
│   └── data/                # Agent data storage
├── venv/                    # Python virtual environment
├── faq_agentcore_app_with_logging.py  # Main agent application with logging
├── .bedrock_agentcore.yaml  # AgentCore configuration file
├── .dockerignore
├── .env                     # Environment variables (not committed)
├── .gitignore
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## 🧠 Architecture Overview

1. **Agent Core Setup** – Configure Amazon Bedrock AgentCore with custom tools
2. **Tool Integration** – Implement search, reformulation, and custom business logic tools
3. **Session Management** – Handle multi-turn conversations with memory persistence
4. **Logging & Observability** – Monitor agent performance with AWS CloudWatch
5. **Invocation Pipeline** – Process user queries through the agent workflow


---

## 🔐 Prerequisites

Before getting started, make sure you have the following:

* ☁️ **AWS Account** with Amazon Bedrock access enabled
* 🐍 **Python 3.9+** installed
* 🔧 **AWS CLI** installed and configured
* 🧠 **Amazon Bedrock Model Access** (request via AWS Console)
* 🤗 **Hugging Face account & token**
* ⚡ **Groq API key**

---

## ⚡ Quick Start

### Step 1: Clone and Set Up Environment

```bash
# Clone the repository
git clone https://github.com/vipunsanjana/Bedrock-AgentCore-AWS-RAG-Hands-On
cd Bedrock-AgentCore-AWS-RAG-Hands-On

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure AWS Credentials

```bash
aws configure
```

Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., `us-east-1`)
- Default output format (e.g., `json`)

### Step 3: Set Up Environment Variables

Create a `.env` file with:

```env
AWS_REGION=us-east-1
BEDROCK_AGENT_ID=your-agent-id
BEDROCK_AGENT_ALIAS_ID=your-alias-id
```

### Step 4: Run the Agent

```bash
# Invoke the agent directly
agentcore invoke "Hello! I want 1kg of almonds"

# Or run the application
python faq_agentcore_app_with_logging.py
```

---

## 🛠️ Agent Tools

The agent includes several built-in tools:

```python
tools = [
    search_faq,           # Search FAQ database
    search_detailed_faq,  # Detailed FAQ search
    reformulate_query     # Query reformulation with context
]
```

### Custom Tool Example

```python
def reformulate_query(original_query: str, focus_aspect: str) -> str:
    """Reformulate user queries with contextual focus"""
    context = "\n\n--\n\n".join(
        f"Entry {i+1}: \n{doc.page_content}"
        for i, doc in enumerate(results)
    )
    logger.info(f"Found {len(results)} entries for aspect: {focus_aspect}")
    return f"Results for '{focus_aspect}' aspect:\n{context}"
```

---

## 🔍 Monitoring & Observability

### View Agent Logs

```bash
# Tail runtime logs
aws logs tail /aws/bedrock-agentcore/runtimes/aws-HaRwD29L0-DEFAULT \
  --log-stream-name-prefix "2026/01/18/[runtime-logs]" \
  --since 1h
```

### Access GenAI Dashboard

Navigate to the **GenAI Dashboard** in AWS Console:
```
https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#gen-ai-observability/agent-core
```

### Session Tracking

Each agent invocation creates a unique session:
- Session ID: `b06c0371-36e6-4ea8-8af3-da327bab040c`
- Request ID: `b672de35-4eb9-4250-856a-3bbf3fe40ffd`

---

## 📊 Example Agent Response

```json
{
  "result": "Hello! We can definitely supply you with 1 kg of almonds. Since the order is below our bulk-discount threshold (5 kg), the price will be the standard retail rate.\n\n**How to place the order**\n\n1. **Add to cart** - On our website, search for 'almonds' and add 1 kg to your cart.\n2. **Checkout** - Proceed to checkout, enter your shipping details, and choose your preferred payment method.\n3. **Confirmation** - You'll receive an order confirmation email with the expected delivery date.\n\nIf you'd like to discuss pricing, shipping options, or have any other questions, just let us know!"
}
```

---

## 🧪 Use Cases

* **Customer Support Agents** – FAQ and troubleshooting
* **Sales Assistants** – Product recommendations and ordering
* **Internal Knowledge Agents** – Company policy and procedure queries
* **Multi-turn Conversations** – Context-aware dialogue systems
* **Specialized Domain Experts** – Industry-specific agent configurations

---

## 🔒 Security & Best Practices

* **Never commit secrets** – Keep `.env` in `.gitignore`
* **Least privilege IAM roles** – Limit agent permissions
* **Secure session handling** – Manage conversation data appropriately
* **Input validation** – Sanitize user inputs before processing
* **Regular dependency updates** – Maintain security patches

---

## 🚀 Deployment Options

1. **Local Development** – Run agent locally for testing
2. **AWS Lambda** – Serverless deployment
3. **Docker Containers** – Containerized agent deployment
4. **Amazon ECS/EKS** – Scalable container orchestration

---

## 🐛 Troubleshooting

### Common Issues

1. **Permission errors** – Ensure IAM roles have Bedrock permissions
2. **Region mismatches** – Verify AWS region consistency
3. **Missing dependencies** – Run `pip install -r requirements.txt`
4. **Session timeouts** – Check agent timeout configurations

### Debug Commands

```bash
# Test AWS Bedrock access
aws bedrock list-foundation-models

# Check agent status
agentcore status

# View recent logs
aws logs get-log-events --log-group-name /aws/bedrock-agentcore/runtimes/aws-HaRwD29L0-DEFAULT --limit 10
```

---

## 📚 Learning Resources

* [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
* [Bedrock AgentCore Developer Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
* [AWS AI/ML Blog](https://aws.amazon.com/blogs/machine-learning/)
* [Bedrock API Reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/)

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🙌 Acknowledgements

* **Amazon Bedrock Team** – For the powerful AgentCore service
* **AWS Community** – For shared knowledge and best practices
* **Open Source Contributors** – For tools and libraries that make this possible

---

## 👨‍💻 Author

**Vipun Sanjana**  
Software Engineer  
Specialized in DevOps & Generative AI  

🔗 GitHub: https://github.com/vipunsanjana  
🔗 LinkedIn: https://www.linkedin.com/in/vipun/  
📧 Email: vipunsanjana34@email.com  
🌐 Portfolio: https://vipunsanjana.dev  

✨ *Build intelligent, conversational agents with Amazon Bedrock AgentCore!*