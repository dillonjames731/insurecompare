import UploadBox from "./components/UploadBox.jsx"
import {useState} from "react"
import ComparisonRow from "./components/ComparisonRow.jsx"
import MonthlyCostCard from "./components/MonthlyCostCard.jsx"
import "./index.css"


function App() {
    const [decFile, setDecFile] = useState(null)
    const [quoteFile, setQuoteFile] = useState(null)
    const [report, setReport] = useState(null)
    const [loading, setLoading] = useState(false)
    const [useAi, setUseAi] = useState(true)
    const [error, setError] = useState(null)

    async function handleCompare() {
        setLoading(true)
        setError(null)
        setReport(null)
        try {
            const form = new FormData()
            form.append("dec_page", decFile)
            form.append("quote_page", quoteFile)
            form.append("use_ai", useAi)

            const response = await fetch("/compare/analyze",
                {method: "POST", body: form})
            if (!response.ok) throw new Error("Comparison failed")
            const report = await response.json()
            setReport(report)
        } catch (error) {
            console.error(error)
            setError("Something went wrong. Please try again.")
        } finally {
                setLoading(false)
            }



    }
    function handleReset(){
        setDecFile(null)
        setQuoteFile(null)
        setReport(null)
        setError(null)
        window.scrollTo({ top: 0, behavior: "smooth" })
    }

    return (
        <main className="min-h-screen bg-slate-50 flex items-center justify-center px-5 py-12">
            <div className="max-w-2xl text-center">
                <p className="text-sm font-medium uppercase tracking-widest text-indigo-600">
                    InsureCompare
                </p>
                <h1 className="mt-3 text-4xl sm:text-5xl font-semibold tracking-tight text-slate-900">
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
                <label className="mt-6 flex items-start gap-3 text-left text-sm text-slate-600">
                    <input type="checkbox" checked={useAi} disabled={loading}
                           onChange={(e) => setUseAi(e.target.checked)}
                           className="mt-0.5 h-4 w-4 accent-indigo-600"/>
                    <span>
                        Use AI to read details our parser can't find. When this is on, the text of your
                        documents is sent to Anthropic's Claude API to be read.
                    </span>
                </label>
                <button type="button" onClick={handleCompare} disabled={!decFile || !quoteFile || loading}
                        className="mt-8 w-full rounded-xl bg-indigo-600 px-6 py-3 text-base font-medium text-white shadow-sm transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:bg-slate-300 inline-flex items-center justify-center gap-2">
                    {loading && <span
                        className="h-5 w-5 animate-spin rounded-full border-2 border-white border-t-transparent"/>}
                    {loading ? "Comparing..." : "Compare"}
                </button>
                {error && <p className="mt-4 text-sm text-red-600">{error}</p>}
                <p className="mt-4 text-xs text-slate-500">
                    Your PDFs are read in memory and never stored on our server.
                </p>

                {report && (

                    <>
                        <p className="mt-8 text-2xl font-semibold text-slate-900 animate-fade-in-up [animation-delay:0ms]">
                            {report.overall_summary}
                        </p>
                        <MonthlyCostCard comparison={report.comparisons.monthly_cost}/>

                        <div className="mt-8 rounded-2xl bg-white p-6 text-left shadow-sm animate-fade-in-up [animation-delay:200ms]">
                            <h2 className="text-sm font-medium uppercase tracking-widest text-slate-500">Coverage
                                limits</h2>
                            <ComparisonRow title="Bodily injury" comparison={report.comparisons.limits.bodily_injury}/>
                            <ComparisonRow title="Property damage"
                                           comparison={report.comparisons.limits.property_damage}/>
                            <ComparisonRow title="Uninsured motorist"
                                           comparison={report.comparisons.limits.uninsured_motorist}/>
                            <ComparisonRow title="Personal injury protection"
                                           comparison={report.comparisons.limits.pip}/>
                            <ComparisonRow title="Medical payments"
                                           comparison={report.comparisons.limits.medical_payments}/>
                        </div>

                        <div className="mt-4 rounded-2xl bg-white p-6 text-left shadow-sm animate-fade-in-up [animation-delay:300ms]">
                            <h2 className="text-sm font-medium uppercase tracking-widest text-slate-500">Deductibles</h2>
                            <ComparisonRow title="Comprehensive"
                                           comparison={report.comparisons.deductibles.comprehensive}/>
                            <ComparisonRow title="Collision" comparison={report.comparisons.deductibles.collision}/>
                        </div>
                        <div className="mt-4 rounded-2xl bg-white p-6 text-left shadow-sm animate-fade-in-up [animation-delay:400ms]">
                            <h2 className="text-sm font-medium uppercase tracking-widest text-slate-500">Add-Ons</h2>
                            <ComparisonRow title="Rental" comparison={report.comparisons.add_ons.rental}/>
                            <ComparisonRow title="Towing" comparison={report.comparisons.add_ons.towing}/>
                        </div>
                         <div className="mt-10 flex items-center justify-center gap-2">
                <button type="button" onClick={handleReset} className="text-sm font-medium text-indigo-600 hover:text-indigo-500">
                    Start Over
                </button>
                         </div>

                    </>
                )}
            </div>

        </main>
    )
}


export default App