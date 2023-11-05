export default function Guest() {
  return (
    <>
      <div className={"d-flex flex-column align-items-center "}>
        <h1 className={"fw-bold mt-4"} style={{ fontSize: "5rem" }}>
          BeerBrain
        </h1>
        <img
          alt={""}
          src={"BeerBrain-nobg.png"}
          style={{ width: "20rem", height: "20rem" }}
        />
        <p
          style={{
            fontSize: "2rem",
            marginTop: "2rem",
          }}
        >
          Don't forget to remind your friends that the <b>beer</b> was not free!
        </p>
      </div>
    </>
  );
}
