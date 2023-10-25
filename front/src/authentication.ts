import { URLS } from "./constants.ts";

export async function signIn(
  username: string,
  password: string,
): Promise<boolean> {
  console.log(`SignIn ${username} by ${password}`);
  const formData = new FormData();
  formData.append("username", username);
  formData.append("password", password);
  const response = await fetch(URLS.get_token, {
    method: "POST",
    body: formData,
  });
  if (!response.ok) {
    return false;
  }
  const json = await response.json();
  const token = json["token"];
  localStorage.setItem("token", token);
  return true;
}

export async function signUp(
  username: string,
  email: string,
  firstname: string,
  lastname: string,
  password: string,
): Promise<boolean> {
  console.log(
    `SignUp ${username} at ${email} of ${firstname} ${lastname} and password ${password}`,
  );
  const formData = new FormData();
  formData.append("username", username);
  formData.append("email", email);
  formData.append("first_name", firstname);
  formData.append("last_name", lastname);
  formData.append("password", password);
  const response = await fetch(URLS.new_user, {
    method: "POST",
    body: formData,
  });
  if (!response.ok) {
    return false;
  }
  return await signIn(username, password);
}

export function signOut(): void {
  localStorage.removeItem("token");
}

export function isAuthorized(): boolean {
  return "token" in localStorage;
}

export default function getAuthHeader() {
  return {
    Authorization: `Token ${localStorage["token"]}`,
  };
}
