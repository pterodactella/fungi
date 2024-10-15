import Chatbot from '@/components/chatbot';
import Head from 'next/head';

export default function Home() {
  return (
    <div>
      <Head>
        <title>Chatbot MVP</title>
        <meta name="description" content="Chatbot interface" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="flex justify-center items-center h-screen">
        <Chatbot />
      </main>
    </div>
  );
}