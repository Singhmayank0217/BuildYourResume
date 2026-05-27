'use client';

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Eye, Download, CheckCircle } from 'lucide-react';
import toast from 'react-hot-toast';
import Header from '../components/Header';
import Button from '../components/Button';
import Card from '../components/Card';
import { getTemplates } from "../services/api";


interface Template {
  id: number;
  name: string;
  description: string;
  structure: any;
  ats_safe: boolean;
  is_recommended: boolean;
}

export default function Templates() {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTemplates = async () => {
      try {
        const response = await getTemplates();
        setTemplates(response.data);
        if (response.data.length > 0) {
          setSelectedTemplate(response.data[0]);
        }
      } catch (error) {
        toast.error('Failed to load templates');
      } finally {
        setLoading(false);
      }
    };

    fetchTemplates();
  }, []);

  const handleSelectTemplate = (template: Template) => {
    setSelectedTemplate(template);
  };

  const handleUseTemplate = (template: Template) => {
    navigate(`/builder?templateId=${template.id}`);
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
          {/* Header */}
          <motion.div className="mb-12" variants={itemVariants}>
            <h1 className="text-4xl font-bold text-neutral-dark mb-4">Resume Templates</h1>
            <p className="text-xl text-gray-600">
              Choose from professional ATS-optimized templates designed for success
            </p>
          </motion.div>

          {loading ? (
            <div className="text-center py-12">
              <motion.div
                className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full mx-auto"
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity }}
              />
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Template List */}
              <motion.div
                className="lg:col-span-1"
                variants={itemVariants}
              >
                <h2 className="text-xl font-bold text-neutral-dark mb-4">Available Templates</h2>
                <div className="space-y-3">
                  {templates.map((template) => (
                    <motion.div
                      key={template.id}
                      whileHover={{ x: 5 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => handleSelectTemplate(template)}
                    >
                      <div
                        className={`p-4 rounded-lg cursor-pointer transition-all ${
                          selectedTemplate?.id === template.id
                            ? 'bg-primary text-white shadow-lg'
                            : 'bg-white text-neutral-dark hover:shadow-md'
                        }`}
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h3 className="font-bold mb-1">{template.name}</h3>
                            {template.is_recommended && (
                              <span className={`inline-block text-xs px-2 py-1 rounded-full ${
                                selectedTemplate?.id === template.id
                                  ? 'bg-white text-primary'
                                  : 'bg-accent text-primary'
                              }`}>
                                Recommended
                              </span>
                            )}
                          </div>
                          {template.ats_safe && (
                            <CheckCircle size={18} />
                          )}
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </motion.div>

              {/* Template Preview */}
              <motion.div
                className="lg:col-span-2"
                variants={itemVariants}
              >
                {selectedTemplate && (
                  <Card className="h-full">
                    {/* Preview Header */}
                    <div className="mb-6">
                      <h2 className="text-3xl font-bold text-neutral-dark mb-2">
                        {selectedTemplate.name}
                      </h2>
                      <p className="text-gray-600 mb-4">{selectedTemplate.description}</p>

                      <div className="flex gap-3 flex-wrap">
                        {selectedTemplate.ats_safe && (
                          <div className="flex items-center gap-2 bg-success bg-opacity-10 text-success px-3 py-2 rounded-lg">
                            <CheckCircle size={18} />
                            <span className="text-sm font-semibold">ATS Optimized</span>
                          </div>
                        )}
                        {selectedTemplate.is_recommended && (
                          <div className="flex items-center gap-2 bg-primary bg-opacity-10 text-primary px-3 py-2 rounded-lg">
                            <span className="text-sm font-semibold">⭐ Recommended</span>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Template Structure Preview */}
                    <div className="bg-neutral rounded-lg p-6 mb-6 max-h-96 overflow-y-auto">
                      <div className="space-y-4 text-sm text-gray-700">
                        {selectedTemplate.structure && Object.entries(selectedTemplate.structure).map(([key, value]) => (
                          <div key={key}>
                            <h4 className="font-bold text-neutral-dark mb-2 uppercase">{key}</h4>
                            <p className="text-gray-500 italic">{String(value)}</p>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex gap-4">
                      <Button
                        onClick={() => handleUseTemplate(selectedTemplate)}
                        size="lg"
                        className="flex-1 bg-gradient-to-r from-primary to-secondary"
                      >
                        <Download size={20} /> Use This Template
                      </Button>
                      <Button
                        variant="outline"
                        size="lg"
                        className="flex-1 bg-transparent"
                      >
                        <Eye size={20} /> Preview Full
                      </Button>
                    </div>
                  </Card>
                )}
              </motion.div>
            </div>
          )}
        </motion.div>
      </main>
    </div>
  );
}
