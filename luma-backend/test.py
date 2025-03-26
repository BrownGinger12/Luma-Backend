from Gateways.Cognito_Gateway import Cognito
resp = Cognito().confirm_user(username="BrownGinga12", confirmation_code="236796")

print(resp)

