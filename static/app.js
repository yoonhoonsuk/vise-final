const { useState, useEffect } = React;

function App() {
  const [models, setModels] = useState([]);
  const [modelA, setModelA] = useState("");
  const [modelB, setModelB] = useState("");
  const [percentA, setPercentA] = useState(60);
  const [modelName, setModelName] = useState("My Blend");
  const [instanceName, setInstanceName] = useState("v1");
  const [blended, setBlended] = useState(null);
  const [error, setError] = useState(null);

  const refreshModels = () =>
    fetch("/api/models")
      .then((r) => r.json())
      .then((data) => {
        setModels(data);
        return data;
      });

  useEffect(() => {
    refreshModels()
      .then((data) => {
        if (data.length >= 2) {
          setModelA(data[0].name);
          setModelB(data[1].name);
        } else if (data.length === 1) {
          setModelA(data[0].name);
          setModelB(data[0].name);
        }
      })
      .catch((e) => setError(String(e)));
  }, []);

  const submitBlend = () => {
    if (!modelA || !modelB) return;
    fetch("/api/blend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model_a: modelA,
        model_b: modelB,
        proportion_a: percentA / 100,
        model_name: modelName,
        instance_name: instanceName,
      }),
    })
      .then((r) => r.json())
      .then((data) => {
        if (data.error) {
          setError(data.error);
          setBlended(null);
        } else {
          setError(null);
          setBlended(data);
          refreshModels().catch((e) => setError(String(e)));
        }
      })
      .catch((e) => setError(String(e)));
  };

  const percentB = 100 - percentA;

  return (
    <div>
      <div className="row">
        <div className="col" style={{ flex: 1 }}>
          <label>New model name</label>
          <input
            type="text"
            value={modelName}
            onChange={(e) => setModelName(e.target.value)}
            placeholder="e.g. My Blend"
          />
        </div>
        <div className="col" style={{ flex: 1 }}>
          <label>Instance name</label>
          <input
            type="text"
            value={instanceName}
            onChange={(e) => setInstanceName(e.target.value)}
            placeholder="e.g. v1"
          />
        </div>
      </div>

      <div className="row" style={{ marginTop: "1rem" }}>
        <div className="col">
          <label>Model A</label>
          <select value={modelA} onChange={(e) => setModelA(e.target.value)}>
            {models.map((m) => (
              <option key={m.name} value={m.name}>{m.name}</option>
            ))}
          </select>
        </div>
        <div className="col">
          <label>Model B</label>
          <select value={modelB} onChange={(e) => setModelB(e.target.value)}>
            {models.map((m) => (
              <option key={m.name} value={m.name}>{m.name}</option>
            ))}
          </select>
        </div>
        <div className="col">
          <label>&nbsp;</label>
          <button onClick={submitBlend}>Submit</button>
        </div>
      </div>

      <div className="slider-block">
        <label>Blend proportion</label>
        <input
          type="range"
          min="0"
          max="100"
          value={percentA}
          onChange={(e) => setPercentA(Number(e.target.value))}
        />
        <div className="props">
          <span>A: {percentA}%</span>
          <span>B: {percentB}%</span>
        </div>
      </div>

      {error && <div style={{ color: "crimson", marginTop: "1rem" }}>{error}</div>}

      {blended && (
        <div>
          <div className="name">{blended.name}</div>
          <div className="total">
            Total weight: {blended.total_weight.toFixed(2)} · {blended.tickers.length} tickers
          </div>
          <table>
            <thead>
              <tr>
                <th>Ticker</th>
                <th className="num">Weight</th>
              </tr>
            </thead>
            <tbody>
              {blended.tickers.map((t) => (
                <tr key={t.symbol}>
                  <td>{t.symbol}</td>
                  <td className="num">{t.weight.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
