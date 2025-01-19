import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { revokeToken } from "@/lib/oauth2-config";

interface UserInfo {
  sub: string;
  name: string;
  email: string;
  username: string;
}

export default function Dashboard() {
  const navigate = useNavigate();
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);

  useEffect(() => {
    const storedUserInfo = localStorage.getItem("user_info");
    if (!storedUserInfo) {
      navigate("/");
      return;
    }
    setUserInfo(JSON.parse(storedUserInfo));
  }, [navigate]);

  const handleLogout = async () => {
    try {
      const accessToken = localStorage.getItem("access_token");
      if (accessToken) {
        await revokeToken(accessToken);
      }

      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("user_info");

      navigate("/");
    } catch (error) {
      console.error("Error during logout:", error);
      // Still clear local storage and redirect even if revoke fails
      localStorage.clear();
      navigate("/");
    }
  };

  if (!userInfo) {
    return null;
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-card rounded-lg shadow p-6">
            <div className="flex justify-between items-center mb-6">
              <h1 className="text-2xl font-semibold">
                Welcome, {userInfo.name}
              </h1>
              <Button variant="destructive" onClick={handleLogout}>
                Log out
              </Button>
            </div>

            <div className="space-y-4">
              <div>
                <h2 className="text-lg font-medium mb-2">User Information</h2>
                <div className="bg-muted rounded-md p-4 space-y-2">
                  <p>
                    <strong>ID:</strong> {userInfo.sub}
                  </p>
                  <p>
                    <strong>Name:</strong> {userInfo.name}
                  </p>
                  <p>
                    <strong>Email:</strong> {userInfo.email}
                  </p>
                  <p>
                    <strong>Username:</strong> {userInfo.username}
                  </p>
                </div>
              </div>

              <div>
                <h2 className="text-lg font-medium mb-2">Access Token</h2>
                <div className="bg-muted rounded-md p-4">
                  <pre className="text-sm overflow-x-auto">
                    {localStorage.getItem("access_token")}
                  </pre>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
