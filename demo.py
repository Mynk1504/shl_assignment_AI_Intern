from app import retrieve_assessments, ExtractedContext

context = ExtractedContext(
    intent='RECOMMEND',
    role='Java Developer',
    seniority='mid',
    skills=['Java', 'Problem Solving'],
    test_preferences=[],
    comparison_tests=[]
)

print('Context:', context.model_dump())

results = retrieve_assessments(context)

print('\nResults found:', len(results))
for r in results:
    print(r['name'], "-", r['url'])
