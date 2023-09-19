export async function signIn(username: string, password: string): Promise<void> {
    console.log(`SignIn ${username} by ${password}`)
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    const response = await fetch("http://127.0.0.1:8000/auth/token/", {method: "POST", body: formData});
    if (response.ok) {
        const json = await response.json()
        const token = json["token"];
        localStorage.setItem("token", token);
    }
}

export async function signUp(username: string, email: string, firstname: string, lastname: string, password: string) {
    console.log(`SignUp ${username} at ${email} of ${firstname} ${lastname} and password ${password}`)
    const formData = new FormData();
    formData.append("username", username);
    formData.append("email", email);
    formData.append("first_name", firstname);
    formData.append("last_name", lastname);
    formData.append("password", password);
    const response = await fetch("http://127.0.0.1:8000/auth/register/", {method: "POST", body: formData});
    if (response.ok) {
        await signIn(username, password);
    }
}