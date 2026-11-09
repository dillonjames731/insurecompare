function ComparisonRow({title, comparison}) {
    return (
        <div className="flex items-start justify-between gap-6 border-b
        border-slate-100 py-4 last:border-b-0">
            <span className="text-sm font-medium text-slate-900">{title}</span>
            <span className="text-right text-sm font-medium text-slate-600">{comparison.summary}</span>
        </div>
    )
}

export default ComparisonRow