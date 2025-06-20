from workflow import Workflow

workflow = Workflow()
result = workflow.run("https://www.github.com/homepage?view=123/123")
print(result.sample_website)
print(result.tech_stack)