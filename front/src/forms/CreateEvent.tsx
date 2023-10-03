import Page from "../components/Page.tsx";
import "./Forms.css"
import "./CreateEvent.css"
import {useForm} from "react-hook-form";
import getAuthHeader from "../auth/authentication.ts";


interface IFormInputs {
    description: string,
}

async function createEventAPI(inputs: IFormInputs) {
    console.log(`Create event ${inputs}`);
    const formData = new FormData();
    formData.append("description", inputs.description);
    const response = await fetch("http://127.0.0.1:8000/core/create-event/", {
        method: "POST",
        headers: getAuthHeader(),
        body: formData
    });
    if (response.ok) {
        const json = await response.json()
        console.log(`Created, ${JSON.stringify(json)}`)
        return json
    }
}

export default function CreateEvent() {
    const {
        register,
        handleSubmit,
        formState: {errors},
    } = useForm<IFormInputs>();


    function onSubmit(data: IFormInputs) {
        console.log(data);
        createEventAPI(data).then((json) => {
            window.location.href = `/events/${json.id}`;
        });
    }

    return (
        <Page>
            <div id={"form-back"}>
                <h1> Create event</h1>
                <form onSubmit={handleSubmit(onSubmit)} method={"POST"}>
                    {/* register your input into the hook by invoking the "register" function */}
                    <label>
                        Description
                        <textarea
                            className={"form-field"} {...register("description", {required: "This field is required"})}/>
                        <span>{errors.description?.message}</span>
                    </label>
                    <input type="submit" value="Submit"/>
                </form>
            </div>
        </Page>
    )
}
