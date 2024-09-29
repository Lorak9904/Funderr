import { useState } from 'react'
import Row from './Row.jsx'

function Rows() {
    const [criteries, setCriteries] = useState({
        ngos: false,
        grants: false,
        companies: false
    })
    let filteredData
    const [data, setData] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(false)

    const retrieveRows = async () => {
        try {
            setLoading(true)
            let res = await fetch("http://192.168.87.179:8080/browse/")
            if (!res.ok)
                throw new Error("res was not okay!")
            res = await res.json()
            let filteredData = []
            if (criteries.ngos) {
                let ngo = res.ngo.map(row => ({ title: row.nazwaOrganizacji, description: row.cel }))
                filteredData = [...filteredData, ...ngo]
            }
            if (criteries.grants) {
                let grants = res.grants.map(row => ({ title: row.nazwa_grantu, description: row.opis }))
                filteredData = [...filteredData, ...grants]
            }
            if (criteries.companies) {
                let companies = res.companies.map(row => ({ title: row.nazwaFirmy, description: row.cel }))
                filteredData = [...filteredData, ...companies]
            }
            setData(filteredData)
        } catch (err) {
            {
                console.log(`err: ${err}`)
                setError(err.message)
            }
        } finally {
            setLoading(false)
        }
    }

    const handleSearch = (e) => {
        e.preventDefault()

        retrieveRows()
    }

    const [search, setSearch] = useState(
        ""
    )

    const [showList, setShowList] = useState(false)

    return (
        <div className='flex-grow flex flex-col justify-start md:w-2/5 mx-auto mt-20'>
            <div className="mb-2 flex flex-row gap-2">
                <form className="w-3/4" onSubmit={handleSearch}>
                    <label for="default-search" className="mb-2 text-sm font-medium text-gray-900 sr-only">Search</label>
                    <div className="relative">
                        <div className="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
                            <svg className="w-4 h-4 text-gray-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
                            </svg>
                        </div>
                        <input onChange={(e) => {
                            setSearch(e.target.value)
                        }} value={search} type="search" id="default-search" class="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500" placeholder="NGOs" required />
                        <button type="submit" class="text-white absolute end-2.5 bottom-2.5 bg-[#F65F6F] hover:bg-[#e27c86] focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2">Search</button>
                    </div>
                </form>
                <div className="relative bg-[#F65F6F] hover:bg-[#e27c86] hover:cursor-pointer flex justify-center items-center rounded-lg flex-grow text-white text-center align-middle">
                    <div className='relative min-w-max' onClick={() => {
                        setShowList(!showList)
                    }} >
                        <p className='font-bold'>Search Criteria</p>
                        <div className='hidden md:block md:absolute -right-4 top-2'>
                            <svg class="w-2.5 h-2.5 ms-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4" />
                            </svg>
                        </div>
                    </div>
                    <ul className={"-bottom-[75px] bg-[#f18e98] px-3 rounded-lg " + (showList ? "absolute" : "hidden")}>
                        <li className='flex flex-row gap-2'>
                            <input id="ck-grants" type="checkbox" checked={criteries.grants} onChange={(e) => {
                                setCriteries((prev) => ({ ...prev, grants: e.target.checked }))
                            }} />
                            <label htmlFor="ck-grants">Grants</label>
                        </li>
                        <li className='flex flex-row gap-2'>
                            <input id="ck-ngos" type="checkbox" checked={criteries.ngos} onChange={(e) => {
                                setCriteries((prev) => ({ ...prev, ngos: e.target.checked }))
                            }} />
                            <label htmlFor="ck-ngos">NGOs</label>
                        </li>
                        <li className='flex flex-row gap-2'>
                            <input id="ck-companies" type="checkbox" checked={criteries.companies} onChange={(e) => {
                                setCriteries((prev) => ({ ...prev, companies: e.target.checked }))
                            }} />
                            <label htmlFor="ck-companies">Companies</label>
                        </li>
                    </ul>
                </div>
            </div>

            {
                loading ? (<p>Loading...</p>) : error ? (<p>The error occured try again!</p>) : data ? (<div className='flex flex-col gap-5'>
                    {
                        data.map(row => {
                            return (<Row title={row.title} description={row.description} />)
                        })
                    }
                </div>) : (<p>Choose the criteria and prompt to start looking</p>)
            }
        </div>
    )
}
export default Rows
