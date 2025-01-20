import { generateCodeVerifier, generateCodeChallenge } from "./pkce";

const OAUTH2_CONFIG = {
  clientId: import.meta.env.VITE_OAUTH_CLIENT_ID,
  clientSecret: import.meta.env.VITE_OAUTH_CLIENT_SECRET,
  redirectUri: `${import.meta.env.VITE_FRONTEND_URL}/callback`,
  authorizationEndpoint: `${import.meta.env.VITE_BACKEND_URL}/o/authorize/`,
  tokenEndpoint: `${import.meta.env.VITE_BACKEND_URL}/o/token/`,
  userinfoEndpoint: `${import.meta.env.VITE_BACKEND_URL}/o/userinfo/`,
  revokeEndpoint: `${import.meta.env.VITE_BACKEND_URL}/o/revoke/`,
  scope: "openid profile email",
};

export async function getAuthorizationUrl(isPopup = false) {
  const codeVerifier = generateCodeVerifier();
  const codeChallenge = await generateCodeChallenge(codeVerifier);

  localStorage.setItem("code_verifier", codeVerifier);

  const params = new URLSearchParams({
    response_type: "code",
    client_id: OAUTH2_CONFIG.clientId,
    redirect_uri: isPopup
      ? `${import.meta.env.VITE_FRONTEND_URL}/callback?popup=true`
      : OAUTH2_CONFIG.redirectUri,
    scope: OAUTH2_CONFIG.scope,
    code_challenge: codeChallenge,
    code_challenge_method: "S256",
  });

  return `${OAUTH2_CONFIG.authorizationEndpoint}?${params.toString()}`;
}

export async function exchangeCodeForTokens(code: string, isPopup = false) {
  const codeVerifier = localStorage.getItem("code_verifier");
  if (!codeVerifier) throw new Error("No code verifier found");

  const response = await fetch(OAUTH2_CONFIG.tokenEndpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization:
        "Basic " +
        btoa(`${OAUTH2_CONFIG.clientId}:${OAUTH2_CONFIG.clientSecret}`),
    },
    body: new URLSearchParams({
      grant_type: "authorization_code",
      code,
      redirect_uri: isPopup
        ? `${import.meta.env.VITE_FRONTEND_URL}/callback?popup=true`
        : OAUTH2_CONFIG.redirectUri,
      code_verifier: codeVerifier,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to exchange code for tokens");
  }

  return response.json();
}

export async function getUserInfo(accessToken: string) {
  const response = await fetch(OAUTH2_CONFIG.userinfoEndpoint, {
    headers: {
      Authorization: `Turbo ${accessToken}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch user info");
  }

  return response.json();
}

export async function revokeToken(token: string) {
  const response = await fetch(OAUTH2_CONFIG.revokeEndpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization:
        "Basic " +
        btoa(`${OAUTH2_CONFIG.clientId}:${OAUTH2_CONFIG.clientSecret}`),
    },
    body: new URLSearchParams({
      token,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to revoke token");
  }
}
