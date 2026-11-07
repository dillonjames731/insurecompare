import UploadBox from "./components/UploadBox.jsx"
import {useState} from "react"


function App() {
    const [decFile, setDecFile] = useState(null)
    const [quoteFile, setQuoteFile] = useState(null)
    const [report, setReport] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    async function handleCompare() {
        setLoading(true)
        setError(null)
        setReport(null)
        try {
            const form = new FormData()
            form.append("dec_page", decFile)
            form.append("quote", quoteFile)

            const uploadResponse = await
                fetch("/compare/upload", {method: "POST", body: form})
            if (!uploadResponse.ok) throw new Error("Upload failed")
            const upload = await uploadResponse.json()
            console.log("upload:", upload)


            const extractResponse = await fetch("/compare/extract", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({comparison_id: upload.comparison_id})
            })
            if (!extractResponse.ok) throw new Error("Extraction failed")


            const report = await extractResponse.json()
            setReport(report)
        } catch (error) {
            console.log(error)
            setError("Something went wrong. Please try again.")
        } finally {
            setLoading(false)
        }


    }

    return (
        <main className="min-h-screen bg-slate-50 flex items-center justify-center px-5">
            <div className="max-w-2xl text-center">
                <p className="text-sm font-medium uppercase tracking-widest text-indigo-600">
                    InsureCompare
                </p>
                <h1 className="mt-3 text-5xl font-semibold tracking-tight text-slate-900">
                    Is your new quote actually better?
                </h1>
                <p className="mt-4 text-lg text-slate-600">
                    Upload your current policy and a new quote. See the price and coverage differences side by side, in
                    plain English. </p>
                <div className="mt-10 grid gap-4 sm:grid-cols-2">
                    <UploadBox label="Current policy" hint="Your declarations page (PDF)" file={decFile}
                               onFileChange={setDecFile}/>
                    <UploadBox label="New quote" hint="The quote you're considering (PDF)" file={quoteFile}
                               onFileChange={setQuoteFile}/>
                </div>
                <button type="button" onClick={handleCompare} disabled={!decFile || !quoteFile || loading}
                        className="mt-8 w-full rounded-xl bg-indigo-600 px-6 py-3 text-base font-medium text-white shadow-sm transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:bg-slate-300 inline-flex items-center justify-center gap-2">
                    {loading && <span
                        className="h-5 w-5 animate-spin rounded-full border-2 border-white border-t-transparent"/>}
                    {loading ? "Comparing..." : "Compare"}
                </button>
                {error && <p className="mt-4 text-sm text-red-600">{error}</p>}


                {report && (
                    <p className="mt-8 text-2xl font-semibold text-slate-900">

                        {report.overall_summary}
                    </p>
                )}
            </div>
        </main>
    )

}

export default App