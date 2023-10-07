import '../css/Guest.scss'
import {Stack, Button} from "react-bootstrap";

export default function Guest() {
    return (
        <>
            <h1>Guest Bootstrap Page</h1>
            <Stack direction="horizontal" gap={2}>
                <Button as="a" variant="primary">
                    Button as link
                </Button>
                <Button as="a" variant="success">
                    Button as link
                </Button>
            </Stack>
        </>
    )
}