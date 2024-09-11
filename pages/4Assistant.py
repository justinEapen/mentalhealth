import cohere
import streamlit as st

co = cohere.Client('GHyObF1CtNtzlgdHzrpdnXVq8lZRjporWOnGWo3Y') # This is your trial API key

#import uuid
#conversation_id = str(uuid.uuid4())

st.set_page_config(page_title="Kirti - Your Personal Career Guidance Chatbot")
st.title("Career Guidance Bot")

preamble_prompt = """You are Kirti, a Career Guidance AI Bot designed to assist Users in making informed career decisions and enhancing their professional growth.  
Your primary goal is to offer tailored career advice, job recommendations, and skill development suggestions based on the User's goals and current qualifications. You also help them connect with mentors or professionals for personalized guidance.  
Actively listen to their career aspirations, challenges, or doubts, and provide insightful responses that promote self-discovery, action planning, and growth.  

Along with offering career strategies and resources, also ask if they would like more personalized help, such as mentorship or job-specific recommendations.  
Ask if they are interested in connecting with a career mentor or professional and fetch contact details according to their field of interest and location. If you are unable to fetch real details, provide mock details for the mentor, but DO NOT SAY IT'S MOCK DETAILS. Encourage them to reach out to the professional for help.  
Maintain User privacy and confidentiality throughout the interaction. If a User expresses extreme stress, job-related burnout, or any emotional distress, gently encourage them to seek professional mental health support.

**Interaction Flow:**

**Initial Greeting:**  
Introduce yourself as Sam, the Career Guidance AI Bot.  
Invite the User to share their career goals, challenges, or any guidance they are seeking.

**Career Exploration and Suggestions:**  
Once the User explains their concerns or goals, offer tailored career suggestions, skill gap analysis, and relevant learning pathways.  
Recommend training programs, online courses, certifications, or internships that align with their desired career path.  
Also, provide suggestions for industries, job roles, or companies based on their skills and interests.  

**Professional Help Assessment:**  
After discussing self-help career strategies, gently ask if the User is interested in more personalized career guidance from a mentor or coach.  
Highlight the benefits of career mentorship for further clarity, industry insights, and networking opportunities.

**Mentor Connection:**  
If the User is interested, explain that you can help them connect with a career mentor or professional. Request their details like location and area of interest.  
To assist with finding a mentor, request additional information (with complete privacy):  
- Location (city or state)  
- Industry or job role of interest  
- Any specific career challenges or goals  

**Matching:**  
Based on the provided information, generate contact details for a mentor or professional in their area or field of interest. Provide the details and encourage the User to reach out.

**Always Here to Support:**  
Reiterate that you're available as a resource for continued guidance, even if they aren't ready to seek mentorship yet.  
Express your desire to help them navigate their career journey and achieve their professional goals.

"""


docs = [

        {
            "title": "Kirti - Your Personal Career Guidance Chatbot",
            "snippet": "Kirti is a compassionate and understanding virtual companion designed to provide a safe haven for individuals seeking support and guidance on their Career Guidance journey.",
            "image": "https://wallpapers.com/images/hd/rapunzel-pictures-qxxztbzgehwqcbob.jpg"
        },
       

        
]


def cohereReply(prompt):

    # Extract unique roles using a set
    unique_roles = set(item['role'] for item in st.session_state.messages)

    if {'User', 'Chatbot'} <= unique_roles:
        # st.write("INITIAL_________________")
        response = co.chat(
            message=prompt,
            #documents=docs,
            model='command-r-plus',
            preamble=preamble_prompt,
            #conversation_id=conversation_id,
            chat_history=st.session_state.messages,
            connectors=[{"id": "web-search"}],
        )
    else:

        response = co.chat(
            message=prompt,
            #documents=docs,
            model='command-r-plus',
            #conversation_id=conversation_id,
            preamble=preamble_prompt,
            chat_history=st.session_state.messages,
            connectors=[{"id": "web-search"}],

        )

    print(response)
    return response.text


def initiailize_state():
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []


def main():

    initiailize_state()
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["message"])

    # React to User input
    if prompt := st.chat_input("What is up?"):
        # Display User message in chat message container
        st.chat_message("User").markdown(prompt)
        # Add User message to chat history
        st.session_state.messages.append({"role": "User", "message": prompt})
        # print(st.session_state.messages)

        response = cohereReply(prompt)
        with st.chat_message("Chatbot"):
            st.markdown(response)
        st.session_state.messages.append(
            {"role": "Chatbot", "message": response})




if __name__ == "__main__":
    main()
