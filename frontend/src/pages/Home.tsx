import { Button } from "@/components/ui/button";
import { getAuthorizationUrl } from "@/lib/oauth2-config";

export default function Home() {
  const handleLogin = async () => {
    const authUrl = await getAuthorizationUrl();
    const width = 500;
    const height = 700;
    const left = window.screenX + (window.outerWidth - width) / 2;
    const top = window.screenY + (window.outerHeight - height) / 2;

    // Store the original window reference
    window.name = "mainWindow";

    window.open(
      authUrl,
      "OAuth Login",
      `width=${width},height=${height},left=${left},top=${top},toolbar=0,location=0,menubar=0,status=0,scrollbars=1`
    );
    // window.location.href = authUrl;
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
