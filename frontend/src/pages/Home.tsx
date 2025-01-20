import { Button } from "@/components/ui/button";
import { getAuthorizationUrl } from "@/lib/oauth2-config";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  const handleLogin = async () => {
    const authUrl = await getAuthorizationUrl(true);
    const width = 500;
    const height = 700;
    const left = window.screenX + (window.outerWidth - width) / 2;
    const top = window.screenY + (window.outerHeight - height) / 2;

    // Clear any existing flags
    localStorage.removeItem("oauth_success");
    localStorage.removeItem("mainWindowUrl");

    const popup = window.open(
      authUrl,
      "OAuth Login",
      `width=${width},height=${height},left=${left},top=${top},toolbar=0,location=0,menubar=0,status=0,scrollbars=1`
    );

    if (!popup) {
      console.error("Popup was blocked");
      return;
    }

    // Poll for popup closure and oauth success
    const checkPopup = () => {
      const pollTimer = setInterval(() => {
        if (!popup || popup.closed) {
          clearInterval(pollTimer);
          const success = localStorage.getItem("oauth_success");
          const userInfo = localStorage.getItem("user_info");

          console.log("Popup closed, checking status:", { success, userInfo }); // Debug log

          if (success && userInfo) {
            localStorage.removeItem("oauth_success");
            navigate("/dashboard");
          }
        }
      }, 500);
    };

    // Start polling after a short delay
    setTimeout(checkPopup, 1000);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-background">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h1 className="text-4xl font-bold text-center">OAuth2 PKCE Demo</h1>
          <p className="mt-3 text-center text-muted-foreground">
            A demonstration of OAuth2 authorization code flow with PKCE
          </p>
        </div>

        <div className="mt-8 space-y-6">
          <Button onClick={handleLogin} className="w-full" size="lg">
            Log in with OAuth2
          </Button>

          <div className="text-sm text-center text-muted-foreground">
            <p>This demo uses:</p>
            <ul className="mt-2 list-disc list-inside">
              <li>OAuth2 Authorization Code Flow</li>
              <li>PKCE (Proof Key for Code Exchange)</li>
              <li>OpenID Connect</li>
              <li>JWT Access Tokens</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
