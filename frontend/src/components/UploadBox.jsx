function UploadBox({label, hint, file, onFileChange}) {
    return (
        <label className="flex cursor-pointer flex-col items-center rounded-2xl border-2 border-dashed border-slate-300 bg-white p-8 transition hover:border-indigo-400 hover:bg-indigo-50">
            <span className="text-base font-medium text-slate-900">{label}</span>
            <span className="mt-1 text-sm text-slate-500"> {file ? file.name : hint}</span>
                <input type="file" accept=".pdf"
                className="hidden" onChange={(event) => {
  onFileChange(event.target.files[0])
  event.target.value = ""
}
                } />
        </label>
        )
        }
        export default UploadBox