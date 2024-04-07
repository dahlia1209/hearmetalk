import { v4 as uuidv4 } from "uuid";

export function oauthSignIn(redirect_uri: string): void {
    // Google's OAuth 2.0 endpoint for requesting an access token
    const oauth2Endpoint: string = 'https://accounts.google.com/o/oauth2/v2/auth';

    const state = uuidv4();
    localStorage.setItem('state', state);

    // Parameters to pass to OAuth 2.0 endpoint.
    const params: { [key: string]: string } = {
        'client_id': import.meta.env.VITE_OAUTH2_CLIENT_ID,
        'redirect_uri': redirect_uri,
        'response_type': 'token',
        'scope': 'https://www.googleapis.com/auth/youtube.force-ssl',
        'include_granted_scopes': 'true',
        'state': state
    };

    // Construct the OAuth URL with parameters.
    const queryString = Object.entries(params).map(([key, value]) =>
        `${encodeURIComponent(key)}=${encodeURIComponent(value)}`
    ).join('&');

    const oauthUrl = `${oauth2Endpoint}?${queryString}`;

    // Open the OAuth URL in a new tab.
    window.open(oauthUrl, '_blank');
}
