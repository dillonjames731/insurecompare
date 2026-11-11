function ComparisonRow({title, comparison}) {
    return (
        <div className="flex items-start flex-col sm:flex-row justify-between gap-1 sm:gap-6 border-b
        border-slate-100 py-4 last:border-b-0">
            <span className="text-sm font-medium text-slate-900">{title}</span>
            <span className="text-sm text-slate-600 text-left sm:text-right">{comparison.summary}</span>
        </div>
    )
}

export default ComparisonRow