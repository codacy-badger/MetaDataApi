from MetaDataApi.users.models import ThirdPartyDataProvider
import json

redirect_uri = "https://meta-data-api.herokuapp.com/oauth2redirect/"

default_data_providers = [
    ThirdPartyDataProvider(
        provider_name="Endomondo",
        api_type="Oauth2-rest",
        api_endpoint="https://api.endomondo.com/api/1/",
        authorize_url="https://www.endomondo.com/oauth/authorize",
        access_token_url="https://api.endomondo.com/oauth/access_token",
        client_id="",
        client_secret="",
        scope=json.dumps([]),
        redirect_uri=redirect_uri,
        rest_endpoints_list=json.dumps([]),
        json_schema_file_url=""
    ),
    ThirdPartyDataProvider(
        provider_name="Withings",
        api_type="Oauth2-rest",
        api_endpoint="https://wbsapi.withings.net/",
        authorize_url="https://account.withings.com/oauth2_user/authorize2",
        access_token_url="https://account.withings.com/oauth2/token",
        client_id="a80378abe1059ef7c415cf79b09b1270f828c4a0fbfdc52dbec06ae5f71b4bb6",
        client_secret="1f1d852451385469a56ef6494cbd2e94c07421c3ee5ffbfca63216079fd36d1a",
        scope=json.dumps([
            # issues with multiple scopes for some reason, but first when i log in
            # "user.info",
            # "user.metrics",
            "user.activity"
        ]),
        redirect_uri=redirect_uri,
        rest_endpoints_list=json.dumps([
            # "v2/user?action=getdevice",
            # "measure?action=getmeas",
            "v2/sleep?action=getsummary&startdateymd={StartDateTime:Y-M-d}&enddateymd={EndDateTime:Y-M-d}",
            "v2/sleep?action=get&startdate={StartDateTime:UTCSEC}&enddate={EndDateTime:UTCSEC}",
        ]),
        json_schema_file_url=""
    ),
    ThirdPartyDataProvider(
        provider_name="Strava",
        api_type="Oauth2-rest",
        api_endpoint="https://www.strava.com/api/v3/",
        authorize_url="https://www.strava.com/oauth/authorize",
        access_token_url="https://www.strava.com/oauth/token",
        client_id="28148",
        client_secret="ed5f469f798830c7214fc8efad54790799fc3ae1",
        scope=json.dumps(["view_private"]),
        redirect_uri=redirect_uri,
        rest_endpoints_list=json.dumps([
            "/activities",
            "/athlete/zones",
            "/athlete"]),
        json_schema_file_url=""
    ),
    ThirdPartyDataProvider(
        provider_name="Oura",
        api_type="Oauth2-rest",
        api_endpoint="https://api.ouraring.com/",
        authorize_url="https://cloud.ouraring.com/oauth/authorize",
        access_token_url="https://api.ouraring.com/oauth/token",
        client_id="Q43N7PFF2RI3SF52",
        client_secret="CX6MEERKWUBIMBMRZOVY6BAAQLF5KDDL",
        scope=json.dumps([
            "email",
            "personal",
            "daily"]),
        redirect_uri=redirect_uri,
        rest_endpoints_list=json.dumps([
            "/v1/userinfo",
            "/v1/sleep?start=YYYY-MM-DD&end=YYYY-MM-DD",
            "/v1/activity?start=YYYY-MM-DD&end=YYYY-MM-DD",
            "/v1/readiness?start=YYYY-MM-DD&end=YYYY-MM-DD"]),
        json_schema_file_url=""
    ),
    ThirdPartyDataProvider(
        provider_name="Google Fit",
        api_endpoint="https://www.googleapis.com/fitness/",
        authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
        access_token_url="https://accounts.google.com/oauth2/v4/token",
        client_id="166351402500-m9302qf47ua66qbr1gdbgrronssnm2v2.apps.googleusercontent.com",
        client_secret="W_jKUZmRCGl05G-TMYuFPbjY",
        scope=json.dumps([
            "https://www.googleapis.com/auth/fitness.activity.read",
        ]),
        redirect_uri=redirect_uri,
        rest_endpoints_list=json.dumps([
            "v1/users/me/dataSources",
        ]),
        json_schema_file_url=""
    ),
    ThirdPartyDataProvider(
        provider_name="template",
        api_endpoint="",
        authorize_url="",
        access_token_url="",
        client_id="",
        client_secret="",
        scope=json.dumps([]),
        redirect_uri=redirect_uri,
        rest_endpoints_list=json.dumps([]),
        json_schema_file_url=""
    ),
]
