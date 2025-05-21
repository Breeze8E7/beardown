# beardown

Welcome to "Bear Down for Boots", a lightweight quiz and feedback engine that helps boot.dev users reinforce learning, monitor progress, and master content through adaptive self-assessment.

As I progressed through boot.dev, I found myself wanting a review tool. Taking notes and re-reading them is nice. Referring to the in-app spellbook is handy. Boots, the built-in AI, is also a great tool. But I wanted something that tests me (and only me, not the AI) and gives me feedback on where I need to study more, and where I am comfortable. I have a teaching background and progress monitoring was a very helpful tool, so I thought maybe I could bring something like that to my boot.dev experience. This tool, when completed, will do the following:  

1) Provide a random sample of 10 questions to the user.  
      a) These questions will be pulled from completed tasks on boot.dev and categorized by Course/Chapter.  
      b) The base version will have manually implemented questions by me, the creator.  
          - An ideal version will tie directly to the user's boot.dev account and pull questions as chapters are completed.  
      c) The base version will only utilize multiple choice questions from boot.dev.  
          - An ideal version will adapt questions that were not originally multiple choice questions into multiple choice.  
          - An ideal version will also allow the user to create their own questions.  

2) Provide feedback on those 10 questions.  
      a) It will track if a question has been answered correctly 3 times in a row.  
          - If this happens, the question is considered "mastered" and will appear less frequently.  
      b) It will also track mastery on a Course/Chapter level so the user can see in more broad strokes.  

3) Adapt the next quiz based on mastery of topics.  
        a) Questions that are considered "mastered" may still appear, but at a much lower frequency.  
