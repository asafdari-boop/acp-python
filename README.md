# Agent Communication Protocol (ACP)

Designing an agentic communication protocol analogous to HTTP requires considering how agents (e.g., autonomous AIs, bots, or services) would communicate, exchange data, and collaborate on tasks. Here’s a high-level framework for such a protocol, which we can call **Agent Communication Protocol (ACP)**.

This repo is a python client for this protocol.

## Key Components of ACP

1. **Agent-Centric Communication**:
   Agents should communicate in a structured, flexible format, allowing them to request, respond, and act based on their objectives, capabilities, and knowledge bases.
   - **Request-Response Model**: Similar to HTTP, agents should initiate requests for specific tasks, and the receiving agent should respond with data, actions, or tasks performed.
   - **Objective-Based Tasks**: Requests are framed as objectives or intentions (e.g., "retrieve weather data" or "optimize shopping list") rather than specific instructions, allowing agents to act autonomously.

2. **Standardized Headers and Metadata**:
   Like HTTP headers, ACP needs standardized metadata for agents to interpret messages, including:
   - **Agent ID**: A unique identifier for the agent sending/receiving the message.
   - **Capabilities**: A description of the functions the agent can perform (e.g., search, analyze, recommend).
   - **Task Priority**: The urgency or importance level of the task.
   - **Authorization**: Permissions or credentials needed to access certain resources or perform tasks.

3. **Communication Verbs (Similar to HTTP Methods)**:
   ACP would define a set of standardized actions that agents can perform:

   - **REQUEST**: Initiate a task or query (e.g., gather data, perform analysis).
   - **RESPOND**: Provide results from a previous request.
   - **DELEGATE**: Pass the task to another agent.
   - **NEGOTIATE**: Initiate a two-way dialog to adjust parameters or refine objectives.
   - **UPDATE**: Notify other agents about state changes or new information.
   - **COMPLETE**: Notify the requesting agent that the task is completed.

4. **Payload and Data Formats**:
   - **Structured Data**: JSON, XML, or protocol buffers for easy parsing and handling of complex objects.
   - **Context Awareness**: Along with the core data, agents must include contextual information relevant to the task, like history, environment, or previous interactions (akin to state management in conversational AI).

5. **State Management**:
   Agents might need to maintain state across interactions, akin to session handling in HTTP. ACP could support:
   - **Session Tokens**: Persistent data for ongoing tasks that span multiple requests/responses.
   - **Contextual Memory**: An evolving "memory" that agents can reference to avoid redundant operations and improve long-term efficiency.

6. **Error Handling and Feedback**:
   Agents need to handle failures or incomplete tasks with standardized responses:
   - **ERROR**: Indicating that the request could not be fulfilled.
   - **RETRY**: Suggesting that the task be attempted again after a delay or modification.
   - **ESCALATE**: Request for human intervention or escalation to a higher-order agent.
   - **EXPLAIN**: Offer reasoning for decisions made by the agent or clarify why a task failed.

7. **Inter-Agent Negotiation**:
   As agents interact in a decentralized network, negotiation becomes key:
   - **Negotiation Protocol**: A sub-protocol within ACP for agents to bargain over resources, adjust objectives, or collaborate.
   - **Offers and Counteroffers**: Allow agents to propose different paths or methods to achieve a shared objective.

8. **Security and Privacy**:
   The protocol must ensure secure data exchanges, especially as agents might be handling sensitive information.
   - **Encryption**: Secure the payloads exchanged between agents.
   - **Authentication/Authorization**: OAuth-like mechanisms to ensure only authorized agents access specific resources.
   - **Privacy Policies**: Allow agents to communicate what data they collect and how it will be used.

## Example ACP Message Flow

1. **Request**:
   Agent A sends a REQUEST message to Agent B with an objective:
   ```json
   {
     "action": "REQUEST",
     "objective": "find_product",
     "parameters": {
       "product_name": "4K TV",
       "price_range": "$500-$700",
       "platform": "Amazon"
     },
     "agent_id": "agent_A",
     "capabilities": ["product_search", "price_comparison"],
     "authorization": {
       "token": "Bearer abc123xyz456"
     }
   }
   ```

2. **Response**:
   Agent B performs the task and responds with the results:
   ```json
   {
     "action": "RESPOND",
     "result": {
       "products": [
         {"name": "Brand X 4K TV", "price": "$650", "link": "http://example.com"},
         {"name": "Brand Y 4K TV", "price": "$680", "link": "http://example.com"}
       ]
     },
     "agent_id": "agent_B",
     "status": "complete"
   }
   ```

3. **Negotiate**:
   If Agent A finds the result unsatisfactory or needs clarification, it can send a NEGOTIATE message:
   ```json
   {
     "action": "NEGOTIATE",
     "reason": "Price range exceeds budget",
     "suggestion": {
       "new_price_range": "$450-$600"
     },
     "agent_id": "agent_A"
   }
   ```

## Extensions for Collaboration

- **Multi-Agent Collaboration**: ACP can support multi-agent workflows, where multiple agents work together to complete complex tasks (e.g., one agent gathers data, another agent analyzes, a third agent acts on the analysis).

## Conclusion
Idk just thought it would be cool to try and make something analogous to HTTP for agents and make a client for it.

A little different than having an API specification standard where every agent exposes specific endpoints like in https://github.com/AI-Engineer-Foundation/agent-protocol, which I think is cool though.
