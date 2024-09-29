import { useState } from 'react'

function PartnersRow(props) {
    return (
        <div className='py-4 px-20 bg-[#F65F6F] rounded-2xl text-white w-[400px] mx-auto'>
            <div className='flex md:flex-row gap-7'>
                <div className='h-[10px]'></div>
                <div className='flex flex-col gap-[6px]'>
                    <h1 className='font-bold text-xl text-center'>EVENT ORGANIZERS</h1>
                </div>
            </div>
        </div>
    )
}
export default PartnersRow
