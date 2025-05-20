import React from 'react';

export default function KickStatus({ status }) {
  return (
    <div className="p-4 text-center">
      <h2 className="text-2xl font-bold">Kick Status</h2>
      <p className="mt-2 text-lg text-gray-700">{status}</p>
    </div>
  );
}