# Manual Testing Required

## What automation cannot cover
- Error message clarity and readability
- API response time under load
- True perceptual distance (the API uses simple RGB distance)
- Documentation accuracy

## Manual test cases
1. Send malformed JSON to see error response
2. Test with extremely long hex strings
3. Test from Postman to check CORS behavior
