import boto3


# Load Cognito details from environment variables
COGNITO_REGION = "us-east-2"
COGNITO_CLIENT_ID = "4dqbmn7piddsf9j6fu61dtou5n"


class Cognito:
    def __init__(self):
        self.cognito_client = boto3.client("cognito-idp", region_name=COGNITO_REGION)
    
    def login_user(self, username: str, password: str):
        try:
            response = self.cognito_client.initiate_auth(
                ClientId=COGNITO_CLIENT_ID,
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": username,
                    "PASSWORD": password
                }
            )
            
            # Extract tokens
            auth_result = response["AuthenticationResult"]
            return {
                "statusCode": 200,
                "AccessToken": auth_result["AccessToken"],
                "IdToken": auth_result["IdToken"],
                "RefreshToken": auth_result["RefreshToken"],
            }

        except self.cognito_client.exceptions.NotAuthorizedException:
            return {"statusCode": 401, "message": "Unauthorized: Incorrect username or password"}

        except self.cognito_client.exceptions.UserNotFoundException:
            return {"statusCode": 404, "message": "User not found"}

        except Exception as e:
            return {"statusCode": 500, "message": f"Internal server error: {str(e)}"}
        
    def confirm_user(self, username: str, confirmation_code: str):
        """Confirm a new user account with a verification code"""
        try:
            response = self.cognito_client.confirm_sign_up(
                ClientId=COGNITO_CLIENT_ID,
                Username=username,
                ConfirmationCode=confirmation_code
            )
            return {"statusCode": 200, "message": "Account confirmed successfully!"}

        except self.cognito_client.exceptions.CodeMismatchException:
            return {"statusCode": 400, "message": "Invalid verification code. Please try again."}

        except self.cognito_client.exceptions.ExpiredCodeException:
            return {"statusCode": 400, "message": "Verification code expired. Please request a new one."}

        except self.cognito_client.exceptions.UserNotFoundException:
            return {"statusCode": 404, "message": "User not found"}

        except Exception as e:
            return {"statusCode": 500, "message": f"Internal server error: {str(e)}"}
    
    def change_password(self, access_token: str, old_password: str, new_password: str):
        """Allows a user to change their password using their old password"""
        try:
            self.cognito_client.change_password(
                PreviousPassword=old_password,
                ProposedPassword=new_password,
                AccessToken=access_token
            )
            return {"statusCode": 200, "message": "Password changed successfully!"}

        except self.cognito_client.exceptions.NotAuthorizedException:
            return {"statusCode": 401, "message": "Unauthorized: Incorrect old password"}

        except self.cognito_client.exceptions.InvalidPasswordException:
            return {"statusCode": 400, "message": "Invalid new password format"}

        except self.cognito_client.exceptions.LimitExceededException:
            return {"statusCode": 429, "message": "Too many password change attempts. Try again later."}

        except Exception as e:
            return {"statusCode": 500, "message": f"Internal server error: {str(e)}"}

