import time
from langchain.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
# =========================================================
# 1. TOOL DEFINITIONS
# =========================================================
@tool
def attendance_calculator(total_classes: int, attended_classes: int) -> str:
    """
    Calculates attendance percentage and exam eligibility status.
    Use this when a student asks if they are eligible for exams or about their attendance percentage.
    Args:
        total_classes: Total number of classes conducted.
        attended_classes: Number of classes attended by the student.
    """
    if total_classes <= 0:
        return "Error: Total classes must be greater than 0."
    
    percentage = (attended_classes / total_classes) * 100
    eligibility = "Eligible for Exam" if percentage >= 75 else " Not Eligible for Exam"
    return f"Attendance: {percentage:.2f}%. Status: {eligibility} (Minimum 75% required)."
@tool
def result_calculator(sub1: float, sub2: float, sub3: float, sub4: float, sub5: float) -> str:
    """
    Calculates average marks, grade, and pass/fail status for 5 subjects.
    Use this when a student provides 5 marks or asks for their grade, average, or result.
    """
    marks = [sub1, sub2, sub3, sub4, sub5]
    average = sum(marks) / 5
    if average >= 90:
        grade = "A"
    elif average >= 75:
        grade = "B"
    elif average >= 60:
        grade = "C"
    else:
        grade = "D"  
    status = " PASS" if average >= 50 else " FAIL"
    return f"Average Marks: {average:.2f}, Grade: {grade}, Status: {status}."
@tool
def fee_balance_calculator(total_course_fee: float, amount_paid: float) -> str:
    """
    Calculates the pending fee balance amount for a student.
    Use this when a student asks about pending fees, due balance, or outstanding course amounts.
    """
    pending = total_course_fee - amount_paid
    return f"Total Course Fee: ₹{total_course_fee:,.2f}, Paid: ₹{amount_paid:,.2f}, Pending Fee Amount: ₹{pending:,.2f}."
@tool
def library_fine_calculator(delayed_days: int) -> str:
    """
    Calculates library fine for a late book return based on delayed days.
    Use this when a student asks about library fines or late penalties.
    """
    if delayed_days <= 0:
        return "No fine. Book returned on time."
    fine = 5 * delayed_days
    return f"Delayed Days: {delayed_days} days. Total Fine Amount: ₹{fine} (Calculated as ₹5 per day)."
@tool
def hostel_fee_calculator(monthly_hostel_fee: float, number_of_months_stayed: int) -> str:
    """
    Calculates total hostel fee based on monthly charges and stay duration.
    Use this when a student asks about hostel accommodation charges or total hostel fees.
    """
    total_fee = monthly_hostel_fee * number_of_months_stayed
    return f"Monthly Fee: ₹{monthly_hostel_fee:,.2f}, Months: {number_of_months_stayed}. Total Hostel Fee: ₹{total_fee:,.2f}."
# =========================================================
# BONUS CHALLENGE: STUDENT INFORMATION TOOL
# =========================================================
STUDENT_DATABASE = {
    "S001": {"name": "Arjun Sharma", "branch": "Computer Science", "semester": 3},
    "S002": {"name": "Priya Patel", "branch": "Electronics", "semester": 5},
    "S003": {"name": "Rahul Kumar", "branch": "Mechanical", "semester": 1}
}
@tool
def student_information(student_id: str) -> str:
    """
    Retrieves profiling details from the college database using a unique Student ID string.
    Use this when someone asks about a student's profile, record, name, or branch.
    """
    s_id = student_id.strip().upper()
    if s_id not in STUDENT_DATABASE:
        return f"Student ID {s_id} not found."
    
    info = STUDENT_DATABASE[s_id]
    return f"Profile found -> Name: {info['name']}, Branch: {info['branch']}, Semester: {info['semester']}."
# =========================================================
# 2. AGENT SETUP & INITIALIZATION
# =========================================================
# Registry containing all tools
tools = [
    attendance_calculator,
    result_calculator,
    fee_balance_calculator,
    library_fine_calculator,
    hostel_fee_calculator,
    student_information
]
# Set up the local model (Ensure Ollama is running)
llm = ChatOllama(model="qwen2.5:3b", temperature=0)
# Construct standard input prompt for tool calling architecture
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an advanced, helpful college student assistant. Use tools to calculate data and look up profiles accurately. Be precise and clean in your answers."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])
# Create the core engine and its runner execution loop
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
# =========================================================
# 3. INTERACTIVE STUDENT CHAT ENGINE
# =========================================================
if __name__ == "__main__":
    print("\n College AI Assistant is ready! (Type 'exit' or 'quit' to stop)\n")
    while True:
        try:
            user_query = input("\nEnter your query: ")
            if user_query.strip().lower() in ['exit', 'quit']:
                print("\n Goodbye! Closing Assistant.")
                break
            if not user_query.strip():
                continue
            print("\n Processing request...")
            response = agent_executor.invoke({"input": user_query})
            print("\n AGENT FINAL ANSWER:")
            print(response["output"])
            print("-" * 50)
        except KeyboardInterrupt:
            print("\n\n Session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n An error occurred: {e}")
