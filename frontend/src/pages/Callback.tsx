import { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { exchangeCodeForTokens, getUserInfo } from "@/lib/oauth2-config";

export default function Callback() {
  const navigate = useNavigate();
  const [error, setError] = useState<string>();
  const processedRef = useRef(false);

  useEffect(() => {
    const handleCallback = async () => {
      if (processedRef.current) return;
      processedRef.current = true;

      try {
        const params = new URLSearchParams(window.location.search);
        const code = params.get("code");
        const isPopup = params.get("popup") === "true";

        if (!code) {
          throw new Error("No authorization code found");
        }

        // Process the tokens with the correct redirect URI
        const tokens = await exchangeCodeForTokens(code, isPopup);
        localStorage.setItem("access_token", tokens.access_token);
        localStorage.setItem("refresh_token", tokens.refresh_token);

        const userInfo = await getUserInfo(tokens.access_token);
        localStorage.setItem("user_info", JSON.stringify(userInfo));

        if (isPopup) {
          console.log("Setting oauth_success flag"); // Debug log
          localStorage.setItem("oauth_success", "true");
          window.close();
          return;
        }

        navigate("/dashboard");
      } catch (err) {
        console.error("Callback error:", err); // Debug log
        setError(err instanceof Error ? err.message : "An error occurred");
      }
    };

    handleCallback();
  }, [navigate]);

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="bg-destructive/10 text-destructive p-4 rounded-md">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <h2 className="text-2xl font-semibold mb-4">Processing Login</h2>
        <div className="animate-pulse text-muted-foreground">
          Please wait while we complete your login...
        </div>
      </div>
    </div>
  );
}
