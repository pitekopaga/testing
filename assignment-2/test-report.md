# Test Report

## AI-Generated Tests
I asked an AI to generate pytest unit tests for the colorblindness function. The AI produced tests for red vs green, red vs blue, identical colors, and case sensitivity.

## Validation Results
- Red vs green: PASS
- Red vs blue: PASS
- Identical colors: PASS
- Case insensitivity: PASS
- Invalid hex format: PLACEHOLDER

## What I Changed
The AI assumed the function would validate hex format. It does not. I left that test as a placeholder to document the gap.

## What I Added
I added tests for green vs green and case insensitivity. The AI missed those.

## Assessment
AI-generated tests are a good starting point but miss edge cases and assume functionality that may not exist. Human review is essential.

## Peer Feedback and Future Improvements
A peer reviewer noted that the current function only handles exact hex matches and does not distinguish between similar shades. He suggested moving to a numerical approach like RGB distance or perceptual color spaces such as LAB. I agree with this feedback. For Assignment 2, I kept the mock simple per the reading's guidance to hardcode responses. In a future iteration, I would implement perceptual distance calculations to handle similar colors and expand the function to cover additional types of colorblindness beyond red-green.

## Professor Feedback
Professor Ong noted that industry best practices for colorblindness include being "color-agnostic" and using differentiating patterns, not just color. I agree. My current function only compares hex codes. A future version would also check for or recommend patterns, icons, or labels to ensure accessibility even when colors are indistinguishable.
