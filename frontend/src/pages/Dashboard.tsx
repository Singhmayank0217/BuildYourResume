'use client';

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FileText, Plus, Zap, Search } from 'lucide-react';
import toast from 'react-hot-toast';
import Header from '../components/Header';
import Button from '../components/Button';
import Card from '../components/Card';
import Input from '../components/Input';
import { getResumes, getOccupations } from "../services/api";



interface Resume {
  id: number;
  title: string;
  ats_score?: number;
  created_at: string;
}

interface Occupation {
  id: number;
  title: string;
  summary_template: string;
  common_skills: string[];
}

export default function Dashboard() {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [occupations, setOccupations] = useState<Occupation[]>([]);
  const [selectedOccupation, setSelectedOccupation] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
  const fetchData = async () => {
    try {
      const [resumesData, occupationsData] = await Promise.all([
        getResumes(),
        getOccupations(),
      ]);

      setResumes(resumesData);
      setOccupations(occupationsData);
    } catch (error) {
      toast.error("Failed to load data");
    } finally {
      setLoading(false);
    }
  };

  fetchData();
}, []);


  const handleSelectOccupation = (occupation: string) => {
    setSelectedOccupation(occupation);
    // This would load the occupation template preview
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 },
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {/* Hero Section */}
          <motion.div className="text-center mb-12" variants={itemVariants}>
            <h1 className="text-4xl font-bold text-neutral-dark mb-4">Smart Resume Builder</h1>
            <p className="text-xl text-gray-600 mb-8">
              Create ATS-optimized resumes that get past applicant tracking systems and land interviews
            </p>
            <div className="flex gap-4 justify-center">
              <Button
                onClick={() => navigate('/builder')}
                size="lg"
                className="bg-gradient-to-r from-primary to-secondary"
              >
                <Plus size={20} /> Build Resume
              </Button>
              <Button
                onClick={() => navigate('/templates')}
                variant="outline"
                size="lg"
              >
                Browse Templates
              </Button>
            </div>
          </motion.div>

          {/* Occupations Section */}
          <motion.div className="mb-12" variants={itemVariants}>
            <h2 className="text-2xl font-bold text-neutral-dark mb-6">Popular Occupations</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {occupations.map((occ) => (
                <motion.div
                  key={occ.id}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => handleSelectOccupation(occ.title)}
                >
                  <Card
                    hoverable
                    className={`cursor-pointer border-2 transition-all ${
                      selectedOccupation === occ.title
                        ? 'border-primary bg-accent'
                        : 'border-transparent'
                    }`}
                  >
                    <div className="flex items-center gap-3 mb-3">
                      <Zap className="text-primary" size={24} />
                      <h3 className="font-bold text-neutral-dark">{occ.title}</h3>
                    </div>
                    <p className="text-sm text-gray-600 mb-3">{occ.summary_template}</p>
                    <div className="flex flex-wrap gap-2">
                      {occ.common_skills.slice(0, 2).map((skill) => (
                        <span
                          key={skill}
                          className="text-xs bg-primary text-white px-2 py-1 rounded-full"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </Card>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* My Resumes Section */}
          <motion.div variants={itemVariants}>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-neutral-dark">My Resumes</h2>
              <Button onClick={() => navigate('/builder')} size="sm" variant="secondary">
                <Plus size={18} /> New Resume
              </Button>
            </div>

            {loading ? (
              <div className="text-center py-12">
                <motion.div
                  className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full mx-auto"
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity }}
                />
              </div>
            ) : resumes.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {resumes.map((resume, index) => (
                  <motion.div
                    key={resume.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <Card
                      onClick={() => navigate(`/builder?resumeId=${resume.id}`)}
                      hoverable
                    >
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <h3 className="font-bold text-lg text-neutral-dark">{resume.title}</h3>
                          <p className="text-sm text-gray-500">
                            {new Date(resume.created_at).toLocaleDateString()}
                          </p>
                        </div>
                        <FileText className="text-primary" size={24} />
                      </div>

                      {resume.ats_score && (
                        <div className="mb-4">
                          <div className="flex justify-between items-center mb-2">
                            <span className="text-sm font-semibold">ATS Score</span>
                            <span className="text-lg font-bold text-success">{resume.ats_score.toFixed(1)}</span>
                          </div>
                          <div className="w-full bg-neutral rounded-full h-2">
                            <motion.div
                              className="bg-gradient-to-r from-primary to-secondary h-2 rounded-full"
                              initial={{ width: 0 }}
                              animate={{ width: `${resume.ats_score}%` }}
                              transition={{ duration: 1, ease: 'easeOut' }}
                            />
                          </div>
                        </div>
                      )}

                      <Button size="sm" className="w-full bg-transparent" variant="outline">
                        Edit Resume
                      </Button>
                    </Card>
                  </motion.div>
                ))}
              </div>
            ) : (
              <Card className="text-center py-12">
                <FileText className="mx-auto mb-4 text-gray-400" size={48} />
                <p className="text-gray-600 mb-6">No resumes yet. Create your first one!</p>
                <Button onClick={() => navigate('/builder')}>
                  Create Resume
                </Button>
              </Card>
            )}
          </motion.div>
        </motion.div>
      </main>
    </div>
  );
}
