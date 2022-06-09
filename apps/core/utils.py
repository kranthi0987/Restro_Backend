from rest_framework import serializers


def email_Register_Validate_Api(request):
    res = {}
    res["success"] = True
    res["errors"] = None
    res["details"] = None
    validation = serializers.EmailUserDataSerializer(data=request)
    if validation.is_valid():
        res["success"] = True
    else:
        res["success"] = False
        res["details"] = "Bad Request Body"
        res["errors"] = validation.errors
    return res